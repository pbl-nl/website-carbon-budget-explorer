<script lang="ts">
	import clsx from 'clsx';

	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import LeafletMap from '$lib/charts/LeafletMap.svelte';
	import { principles } from '$lib/principles';
	import ShareTabs from '$lib/ShareTabs.svelte';
	import MiniPathwayCard from '$lib/MiniPathwayCard.svelte';
	import AllocationCard from '$lib/AllocationCard.svelte';
	import type { GeoJSON } from 'geojson';

	import type { PageData } from './$types';
	import GlobalQueryCard from '$lib/GlobalQueryCard.svelte';
	import GlobalBudgetCard from '$lib/GlobalBudgetCard.svelte';
	import RegionList from '$lib/RegionList.svelte';
	import Sidebar from '$lib/Sidebar.svelte';

	export let data: PageData;

	let clickedFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined;
	const gotoRegion = (
		feature?: GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
	) => {
		if (browser) {
			const region = feature?.properties?.ISO_A3_EH;
			if (region !== undefined && region !== '') {
				goto(`/regions/${region}${$page.url.search}`);
			}
		}
	};
	$: gotoRegion(clickedFeature);

	function updateQueryParam(name: string, value: string) {
		if (browser) {
			const params = new URLSearchParams($page.url.search);
			// TODO get called once instead of currently being called twice
			if (params.get(name) !== value) {
				params.set(name, value);
				goto(`?${params.toString()}`);
			}
		}
	}

	function selectEffortSharing(value: string) {
		data.effortSharing = value as keyof typeof principles;
	}

	function changeEffortSharing(value: keyof typeof principles | undefined) {
		if (value !== undefined) {
			updateQueryParam('effortSharing', value);
		}
	}
	$: changeEffortSharing(data.effortSharing);

	let allocationTime = '2030';
	function updateAllocationTime(allocationTime: string) {
		updateQueryParam('allocTime', allocationTime);
	}
	$: updateAllocationTime(allocationTime);

	let hoveredFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined;
	$: hoveredMetric = hoveredFeature
		? data.metrics.data.find((m) => m.ISO === hoveredFeature!.properties!.ISO_A3_EH)
		: undefined;
</script>

<div class="flex h-full gap-4">
	<Sidebar>
		<GlobalBudgetCard
			remaining={data.pathway.stats.co2.remaining}
			relative={data.pathway.stats.co2.relative}
		/>
		<GlobalQueryCard
			choices={data.pathway.choices}
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
						{#if hoveredFeature && hoveredFeature.properties && hoveredMetric}
							<div>
								{hoveredFeature.properties.NAME}
							</div>
							<div>
								{hoveredMetric.value.toFixed(0)} tonnes CO₂e per capita
							</div>
						{:else}
							<div>Click on a country or</div>
							<details class="dropdown">
								<summary class="btn-ghost btn-sm btn w-60 font-normal"
									>Select country &#9660;</summary
								>
								<!-- TODO dont hardcode height and width -->
								<div
									class="compact card dropdown-content rounded-box z-[500] h-[600px] w-[900px] overflow-y-scroll bg-base-100 shadow"
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
							{#each Object.entries(principles) as [id, { label, summary }]}
								<button
									class={clsx(
										'tooltip h-16 flex-1 rounded border-2 text-center shadow-lg before:w-36',
										data.effortSharing === id ? 'btn-neutral' : 'btn-outline bg-base-100'
									)}
									disabled={data.effortSharing === id}
									on:click={() => selectEffortSharing(id)}
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
