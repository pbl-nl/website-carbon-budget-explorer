<script lang="ts">
	import { run } from 'svelte/legacy';

	import { Map as LMap, GeoJSON, ControlAttribution, Tooltip } from 'sveaflet';
	import * as L from 'leaflet';
	// Load proj4leaflet plugin so L.Proj.CRS is available
	import 'proj4leaflet';
	import 'leaflet/dist/leaflet.css';
	import { browser } from '$app/environment';
	import { interpolateYlGnBu, scaleSequential } from 'd3';
	import ColorLegend from './components/ColorLegend.svelte';
	import type { BordersCollection, BudgetSpatial, SpatialMetric } from '$lib/api';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import type { GeoJSONOptions, MapOptions, GeoJSON as GeoJSONT, LeafletMouseEvent } from 'leaflet';
	import type { Feature, Geometry } from 'geojson';

	const robinson = new L.Proj.CRS(
		'ESRI:54030',
		'+proj=robin +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs',
		{
			resolutions: [131072, 65536, 32768, 16384, 8192, 4096, 2048]
		}
	);

	const mapOptions: MapOptions = {
		center: [10, 20],
		zoom: 3,
		minZoom: 2,
		zoomControl: false,
		crs: robinson,
		attributionControl: false
	};

	const interpolator = interpolateYlGnBu;

	function getMetric(feature: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>) {
		return metricsLookup.get(feature.properties!.ISO_A3_EH);
	}

	interface Props {
		borders: BordersCollection;
		metrics: BudgetSpatial<SpatialMetric>;
		clickedFeature: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties> | undefined;
	}

	let { borders, metrics, clickedFeature = $bindable() }: Props = $props();
	const metricsLookup = $derived(new Map(metrics.data.map((m) => [m.Region, m])));

	type RegionFeature = Feature<Geometry, { ISO_A3_EH: string; NAME: string }>;

	interface TooltipContent {
		latlng: L.LatLng;
		name: string;
		metric?: number;
	}

	let tooltip: TooltipContent | undefined = $state(undefined);

	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedDomain = tweened(metrics.domain, tweenOptions);

	function onClick(e: LeafletMouseEvent) {
		clickedFeature = e.sourceTarget.feature.properties;
		// <GeoJSON> dts says e is a LeafletMouseEvent but it is not
		// it is CustomEvent with e.detail being the LeafletMouseEvent
	}

	function onMouseOver(e: LeafletMouseEvent) {
		e.sourceTarget.setStyle({
			weight: 1,
			color: 'black'
		});
		e.sourceTarget.bringToFront();

		const feature: RegionFeature = e.sourceTarget.feature;
		const metric = getMetric(feature);
		tooltip = {
			latlng: e.latlng,
			name: feature.properties!.NAME,
			metric: metric?.value
		};
	}

	function onmouseout(e: LeafletMouseEvent) {
		e.sourceTarget.setStyle({
			weight: 1,
			color: 'darkgrey'
		});
		tooltip = undefined;
	}

	run(() => {
		tweenedDomain.set(metrics.domain);
	});
	let scale = $derived(
		scaleSequential().clamp(true).domain($tweenedDomain).interpolator(interpolator)
	);

	function styleBuilder(data: Props['metrics']['data']) {
		return function (geoJsonFeature: RegionFeature | undefined) {
			if (geoJsonFeature === undefined) {
				return {};
			}
			const value = getMetric(geoJsonFeature)?.value;
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
		<LMap options={mapOptions}>
			<GeoJSON json={borders} options={geoJsonOptions} bind:instance={geojsonlayer} />
			<ControlAttribution
				options={{
					prefix: false
				}}
			/>
			{#if tooltip}
				<Tooltip latLng={tooltip.latlng} class="text-base">
					<div>
						{tooltip.name}
					</div>
					<div>
						{#if tooltip.metric}
							{tooltip.metric.toFixed(0)} tonnes CO₂e per capita
						{:else}
							No data available
						{/if}
					</div>
				</Tooltip>
			{/if}
		</LMap>
		<ColorLegend title={'Emissions allocation per capita (t CO2e/pc)'} {scale} />
	{/if}
</div>

<style>
	:global(.leaflet-container) {
		background-color: transparent;
	}
</style>
