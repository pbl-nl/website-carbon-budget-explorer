<script lang="ts">
	import { run } from 'svelte/legacy';

	import { Map, GeoJSON, TileLayer } from 'sveaflet';
	// import {CRS} from 'leaflet?client'
	import type { BordersCollection } from '$lib/server/db/borders';
	import 'leaflet/dist/leaflet.css';
	import { browser } from '$app/environment';
	import { interpolateYlGnBu, scaleSequential } from 'd3';
	import ColorLegend from './components/ColorLegend.svelte';
	import type { BudgetSpatial, SpatialMetric } from '$lib/api';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import type { GeoJSONOptions, MapOptions, GeoJSON as GeoJSONT, LeafletMouseEvent } from 'leaflet';
	import type { Feature, Geometry } from 'geojson';

	const mapOptions: MapOptions = {
		center: [30, 5],
		zoom: 3,
		minZoom: 2,
		zoomControl: false
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

	const interpolator = interpolateYlGnBu;

	function getMetric(
		feature: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>,
		metrics: SpatialMetric[]
	) {
		return metrics.find((m) => m.ISO === feature.properties!.ISO_A3_EH);
	}

	interface Props {
		borders: BordersCollection;
		metrics: BudgetSpatial<SpatialMetric>;
		clickedFeature: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties> | undefined;
		hoveredFeature: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties> | undefined;
	}

	let {
		borders,
		metrics,
		clickedFeature = $bindable(),
		hoveredFeature = $bindable()
	}: Props = $props();

	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedDomain = tweened(metrics.domain, tweenOptions);

	function onClick(e: LeafletMouseEvent) {
		clickedFeature = e.sourceTarget.feature.properties;
		// <GeoJSON> dts says e is a LeafletMouseEvent but it is not
		// it is CustomEvent with e.detail being the LeafletMouseEvent
	}

	function onMouseOver(e: LeafletMouseEvent) {
		hoveredFeature = e.sourceTarget.feature;
	}

	function onmouseout() {
		hoveredFeature = undefined;
	}

	run(() => {
		tweenedDomain.set(metrics.domain);
	});
	let scale = $derived(
		scaleSequential().clamp(true).domain($tweenedDomain).interpolator(interpolator)
	);

	function styleBuilder(data: Props['metrics']['data']) {
		return function (geoJsonFeature: Feature<Geometry, { ISO_A3_EH: string }> | undefined) {
			if (geoJsonFeature === undefined) {
				return {};
			}
			const value = getMetric(geoJsonFeature, data)?.value;
			// TODO Deal with nans?
			const defaultOptions = { fillColor: 'grey', color: 'darkgrey', weight: 1 };
			if (value === undefined) {
				return defaultOptions;
			} else {
				return { ...defaultOptions, fillColor: scale(value), fillOpacity: 0.8 };
			}
		};
	}

	const geoJsonOptions: GeoJSONOptions = {
		style: styleBuilder(metrics.data)
	};

	let geojsonlayer: GeoJSONT | undefined = $state(undefined);

	$effect(() => {
		if (geojsonlayer) {
			geojsonlayer.on('click', onClick);
			geojsonlayer.on('mouseover', onMouseOver);
			geojsonlayer.on('mouseout', onmouseout);
		}
		return () => {
			if (geojsonlayer) {
				geojsonlayer.off('click', onClick);
				geojsonlayer.off('mouseover', onMouseOver);
				geojsonlayer.off('mouseout', onmouseout);
			}
		};
	});

	$effect(() => {
		if (geojsonlayer) {
			geojsonlayer.setStyle(styleBuilder(metrics.data));
		}
	});
</script>

<div class="h-full w-full" id="leaflet-wrapper">
	{#if browser}
		<Map options={mapOptions}>
			<TileLayer url={tileUrl} options={tileLayerOptions} />
			<GeoJSON json={borders} options={geoJsonOptions} bind:instance={geojsonlayer} />
		</Map>
		<ColorLegend title={'Emissions allocation per capita (t CO2e/pc)'} {scale} />
	{/if}
</div>

<style>
	:global(.leaflet-container) {
		background-color: transparent;
	}
</style>
