<script lang="ts">
	import { slide } from 'svelte/transition';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import GlobalBudgetForm from '$lib/PathwayForm.svelte';
	import RegionFilter from '$lib/RegionFilter.svelte';
	import LeafletMap from '$lib/charts/LeafletMap.svelte';
	import type { GeoJSON } from 'geojson';

	import { principles } from '$lib/principles';
	import type { PageData } from './$types';

	export let data: PageData;

	let region: string;
	const gotoRegion = (region: string) => {
		if (browser && region !== undefined && region !== '') {
			goto(`/regions/${region}${$page.url.search}`);
		}
	};
	$: gotoRegion(region);

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

	function changeVariable(value: string) {
		updateQueryParam('variable', value);
	}
	$: changeVariable(data.variable);

	function selectEffortSharing(value: string) {
		data.effortSharing = value as keyof typeof principles;
	}

	function changeEffortSharing(value: keyof typeof principles | undefined) {
		if (value !== undefined) {
			updateQueryParam('effortSharing', value);
		}
	}
	$: changeEffortSharing(data.effortSharing);

	let showCountriesPanel = false;
	let showSettngsPanel = false;

	let selectedFeature:
		| GeoJSON.Feature<GeoJSON.GeometryObject, GeoJSON.GeoJsonProperties>
		| undefined;
	$: selectedMetric = selectedFeature
		? data.metrics.find((m) => m.ISO === selectedFeature!.properties!.ISO_A3_EH)
		: undefined;
</script>

<main class="flex h-full max-h-full w-full flex-row gap-2">
	<div class="flex grow flex-col">
		<div class="relative h-full w-full">
			<div class="absolute left-4 top-4 z-[500] bg-slate-50 p-2 shadow-lg">
				<button class="text-3xl" on:click={() => (showSettngsPanel = !showSettngsPanel)}>⚙</button>
				{#if showSettngsPanel}
					<div>
						<!-- TODO if variable is temp then disable warming temp radio group -->
						<GlobalBudgetForm
							choices={data.pathway.choices}
							query={data.pathway.query}
							onChange={updateQueryParam}
						/>
						<div class="flex flex-col pt-4">
							<h2>CO2 budget</h2>
							<label>
								<input
									disabled
									type="radio"
									name="variable"
									value="2030"
									bind:group={data.variable}
								/>
								in 2030
							</label>
							<label>
								<input
									disabled
									type="radio"
									name="variable"
									value="2040"
									bind:group={data.variable}
								/>
								in 2040
							</label>
							<label>
								<input type="radio" name="variable" value="2100" bind:group={data.variable} />
								full century
							</label>
						</div>
					</div>
				{/if}
			</div>
			<div
				class="absolute inset-x-1/3 top-0 z-[500] flex flex-row justify-between rounded-b-md bg-white p-2 shadow-lg"
			>
				{#if !data.effortSharing}
					<div>Select an effort sharing principle below.</div>
				{/if}
				<div>
					{#if selectedFeature && selectedFeature.properties}
						<a
							href={`/regions/${selectedFeature.properties.ISO_A3_EH}${$page.url.search}`}
							class="mb-1 mr-2 rounded-lg bg-gradient-to-br from-green-400 to-blue-600 px-5 py-2 text-white hover:bg-gradient-to-bl focus:outline-none focus:ring-4 focus:ring-green-200 dark:focus:ring-green-800"
							>{selectedFeature.properties.NAME}</a
						>
					{:else}
						Click on a region to see more information.
					{/if}
				</div>

				<div>
					{#if selectedFeature && selectedFeature.properties && selectedMetric}
						<!-- TODO replace with key indicators -->
						{selectedMetric.value > 1_000
							? `${(selectedMetric.value / 1_000).toPrecision(3)} Gt CO2`
							: `${selectedMetric.value.toPrecision(3)} Mt CO2`}
					{/if}
				</div>
			</div>
			<div class="h-full w-full">
				<div class="flex h-full w-full items-center justify-center bg-white">
					<LeafletMap borders={data.borders} metrics={data.metrics} bind:selectedFeature />
				</div>
			</div>
			<div class="absolute bottom-2 z-[500] flex w-full flex-row justify-center gap-2">
				{#each Object.entries(principles) as [id, { label, summary }]}
					<button
						class={data.effortSharing === id
							? 'h-38 relative w-48 border-2 border-orange-950 bg-orange-400 object-center text-center shadow-lg'
							: 'h-38 relative w-48 border-2 bg-orange-200 object-top text-center shadow-lg'}
						disabled={data.effortSharing === id}
						on:click={() => selectEffortSharing(id)}
					>
						<p class="text-xl">{label}</p>
						<p class="text-sm">{summary}</p>
						<a
							class="absolute right-1 top-1 inline-block text-xl"
							title="More information"
							target="_blank"
							rel="noopener"
							href={`/about#${id}`}>ⓘ</a
						>
					</button>
				{/each}
			</div>
		</div>
	</div>
	<!-- TODO make region filter have own scroll bar and not move map down -->
	<div class="max-h-screen overflow-y-auto">
		<button
			title={showCountriesPanel ? 'Click to hide region list' : 'Click to search for region'}
			on:click={() => (showCountriesPanel = !showCountriesPanel)}
		>
			<span class={showCountriesPanel ? 'countries-panel-shown' : 'countries-panel-hidden'}
				>{showCountriesPanel ? '↦' : '↧'} Find region</span
			>
		</button>
		{#if showCountriesPanel}
			<div transition:slide={{ axis: 'x' }}>
				<RegionFilter regions={data.metrics} searchParams={$page.url.search} />
			</div>
		{/if}
	</div>
</main>

<style>
	.countries-panel-hidden {
		text-orientation: sideways;
		writing-mode: vertical-rl;
	}
	.countries-panel-shown {
		text-orientation: upright;
		writing-mode: horizontal-tb;
	}
</style>
