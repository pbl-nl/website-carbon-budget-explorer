<script lang="ts">
	import { LeafletMap, GeoJSON, TileLayer } from 'svelte-leafletjs?client';
	// import {CRS} from 'leaflet?client'
	import type { BordersCollection } from '$lib/server/db/borders';
	import 'leaflet/dist/leaflet.css';
	import { browser } from '$app/environment';
	import type { GeoJSONOptions, MapOptions } from 'leaflet';
	import { interpolateYlGnBu, scaleSequential } from 'd3';
	import ColorLegend from './components/ColorLegend.svelte';
	import type { BudgetSpatial, SpatialMetric } from '$lib/api';

	export let borders: BordersCollection;
	export let metrics: BudgetSpatial<SpatialMetric>;

	const mapOptions: MapOptions = {
		center: [30, 5],
		zoom: 3,
		minZoom: 2,
		zoomControl: false
		// TODO when open street map is not shown render less gray background
	};
	if (browser) {
		// mapOptions.crs = CRS.EPSG4326
	}

	const tileUrl = 'https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.{ext}';
	const tileLayerOptions = {
		minZoom: 4,
		maxZoom: 20,
		maxNativeZoom: 19,
		attribution:
			'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
		ext: 'png',
		subdomains: 'abcd'
	};

	let tileLayer;

	function colors(specifier: string) {
		var n = (specifier.length / 6) | 0,
			colors = new Array(n),
			i = 0;
		while (i < n) colors[i] = '#' + specifier.slice(i * 6, ++i * 6);
		return colors;
	}

	const interpolator = interpolateYlGnBu;
	$: scale = scaleSequential().clamp(true).domain(metrics.domain).interpolator(interpolator); // TODO configurable colormap?

	function getColor(d: number) {
		return scale(d);
	}
	// TODO Deal with nans?
	// TODO add colorbar

	function getMetric(
		feature: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>,
		metrics: SpatialMetric[]
	) {
		return metrics.find((m) => m.ISO === feature.properties!.ISO_A3_EH);
	}

	const geoJsonOptions: GeoJSONOptions = {
		style: function (geoJsonFeature) {
			if (geoJsonFeature === undefined) {
				return {};
			}
			const value = getMetric(geoJsonFeature, metrics.data)?.value;
			const defaultOptions = { fillColor: 'grey', color: 'darkgrey', weight: 1 };
			if (value === undefined) {
				return defaultOptions;
			} else {
				return { ...defaultOptions, fillColor: getColor(value), fillOpacity: 0.8 };
			}
		}
	};

	export let clickedFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined;
	export let hoveredFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined;

	function onClick(e: any) {
		clickedFeature = e.detail.sourceTarget.feature;
		// <GeoJSON> dts says e is a LeafletMouseEvent but it is not
		// it is CustomEvent with e.detail being the LeafletMouseEvent
	}

	function onMouseOver(e: any) {
		hoveredFeature = e.detail.sourceTarget.feature;
	}

	function onmouseout() {
		hoveredFeature = undefined;
	}

	let leafletMap: LeafletMap;

	// @types/svelte-leafletjs is missing GeoJSON.data property
	// use any to avoid type errors,
	// see https://github.com/sveltejs/language-tools/issues/1026#issuecomment-1002839154
	const notypecheck = (x: any) => x;
</script>

<div class="h-full w-full" id="leaflet-wrapper">
	{#if browser}
		<LeafletMap bind:this={leafletMap} options={mapOptions}>
			<TileLayer bind:this={tileLayer} url={tileUrl} options={tileLayerOptions} />
			<GeoJSON
				{...notypecheck({ data: borders })}
				options={geoJsonOptions}
				events={['click', 'mouseover', 'mouseout']}
				on:click={onClick}
				on:mouseover={onMouseOver}
				on:mouseout={onmouseout}
			/>
		</LeafletMap>
		<ColorLegend title={'tonnes CO₂e per capita'} {...notypecheck({ scale: scale })} {scale} />
	{/if}
</div>

<style>
	:global(.leaflet-container) {
		background-color: transparent;
	}
</style>
