<script lang="ts">
	import { run } from 'svelte/legacy';

	import clsx from 'clsx';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import LeafletMap from '$lib/charts/LeafletMap.svelte';
	import { allocationMethods } from '$lib/allocationMethods';
	import ShareTabs from '$lib/ShareTabs.svelte';
	import MiniPathwayCard from '$lib/MiniPathwayCard.svelte';
	import AllocationCard from '$lib/AllocationCard.svelte';
	import type { PageData } from './$types';
	import GlobalQueryCard from '$lib/GlobalQueryCard.svelte';
	import GlobalBudgetCard from '$lib/GlobalBudgetCard.svelte';
	import RegionList from '$lib/RegionList.svelte';
	import Sidebar from '$lib/Sidebar.svelte';
	// eslint wants import below, while ts works without
	import type { GeoJSON } from 'geojson';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let clickedFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined = $state();
	const gotoRegion = (
		feature?: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
	) => {
		if (browser) {
			const properties = feature as unknown as { ISO_A3_EH: string };
			const region = properties?.ISO_A3_EH;
			if (region !== undefined && region !== '') {
				goto(`/regions/${region}${$page.url.search}`);
			}
		}
	};
	$effect(() => {
		gotoRegion(clickedFeature);
	});

	function updateQueryParam(name: string, value: string) {
		if (browser) {
			const params = new URLSearchParams($page.url.search);
			// TODO get called once instead of currently being called twice
			if (params.get(name) !== value) {
				params.set(name, value);
				// console.log('goto', `?${params.toString()}`);
				goto(`?${params.toString()}`);
			}
		}
	}

	function selectAllocationMethod(value: string) {
		updateQueryParam('allocationMethod', value);
	}

	let allocationTime = $state('2030');
	function updateAllocationTime(allocationTime: string) {
		updateQueryParam('allocTime', allocationTime);
	}
	run(() => {
		updateAllocationTime(allocationTime);
	});

	let hoveredFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined = $state();
	let hoveredMetric = $derived(
		hoveredFeature
			? data.metrics.data.find((m) => m.Region === hoveredFeature!.properties!.ISO_A3_EH)
			: undefined
	);
</script>

<div class="flex h-full gap-4">
	<Sidebar>
		<GlobalBudgetCard
			remaining={data.global.budget.remaining}
			relative={data.global.budget.relative}
		/>
		<GlobalQueryCard
			options={data.pathway.options}
			query={data.pathway.query}
			onChange={updateQueryParam}
		/>
		<AllocationCard bind:allocationTime />
		<div class="hidden 2xl:flex 2xl:flex-1">
			<MiniPathwayCard global={data.global} />
		</div>
	</Sidebar>
	<div class="flex grow flex-col">
		<ShareTabs />
		<div class="flex h-full max-h-full w-full flex-row gap-2">
			<div class="flex grow flex-col">
				<div class="relative h-full w-full">
					<div
						class="absolute left-0 top-0 z-[500] min-h-[4.5rem] w-64 rounded-br-md bg-white p-2 shadow"
					>
						{#if hoveredFeature && hoveredFeature.properties}
							<div>
								{hoveredFeature.properties.NAME}
							</div>
							<div>
								{#if hoveredMetric}
									{hoveredMetric.value.toFixed(0)} tonnes CO₂e per capita
								{:else}
									No data available
								{/if}
							</div>
						{:else}
							<div>Click on a country or</div>
							<details class="dropdown">
								<summary class="btn btn-ghost btn-sm w-60 font-normal"
									>Select country &#9660;</summary
								>
								<!-- TODO dont hardcode height and width -->
								<div
									class="card dropdown-content compact rounded-box z-[500] h-[600px] w-[900px] overflow-y-scroll bg-base-100 shadow"
								>
									<!-- TODO add filter input box to make it easier to find country -->
									<div class="card-body">
										<RegionList regions={data.regions} />
									</div>
								</div>
							</details>
						{/if}
					</div>
					<div class="h-full w-full">
						<div class="flex h-full w-full items-center justify-center bg-white">
							<LeafletMap
								borders={data.borders}
								metrics={data.metrics}
								bind:clickedFeature
								bind:hoveredFeature
							/>
						</div>
					</div>
					<div class="absolute bottom-2 z-[400] w-full">
						<div class="flex w-full flex-row justify-center gap-2 p-2">
							<div class="prose text-lg font-bold">Choose a method of allocation:</div>
						</div>
						<div class="flex w-full flex-row content-stretch justify-stretch gap-2 p-2">
							{#each Object.entries(allocationMethods) as [id, { label, summary }]}
								<button
									class={clsx(
										'tooltip h-16 flex-1 rounded border-2 text-center shadow-lg before:w-36',
										data.allocationMethod === id ? 'btn-neutral' : 'btn-outline bg-base-100'
									)}
									disabled={data.allocationMethod === id}
									onclick={() => selectAllocationMethod(id)}
									data-tip={summary}
								>
									{label}
								</button>
								<!-- TODO bring back link to about page? -->
							{/each}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
