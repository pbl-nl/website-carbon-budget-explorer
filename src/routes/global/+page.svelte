<script lang="ts">
	import { run } from 'svelte/legacy';

	import Sidebar from '$lib/Sidebar.svelte';

	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { page } from '$app/state';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { tour } from '$lib/shared/stores';
	import ShareTabs from '$lib/ShareTabs.svelte';
	import Pathway from '$lib/charts/Pathway.svelte';
	import Line from '$lib/charts/components/Line.svelte';
	import Area from '$lib/charts/components/Area.svelte';
	import Gap from '$lib/charts/components/Gap.svelte';

	import type { PageData } from '../global/$types';
	import GlobalBudgetCard from '$lib/GlobalBudgetCard.svelte';
	import GlobalQueryCard from '$lib/GlobalQueryCard.svelte';
	import { onMount } from 'svelte';

	import { driver } from 'driver.js';
	import 'driver.js/dist/driver.css';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
	const driverObj = driver({
		steps: [
			{
				element: '#globalquerycard',
				popover: {
					title: 'Set global targets',
					description:
						'In these sliders, set your targets on temperature, risk and negative emissions, which affect the global emissions pathway'
				}
			},
			{
				element: '#references',
				popover: {
					title: 'Compare with other pathways',
					description: 'Tick these boxes to show other types of emissions pathways on the graph'
				}
			},
			{
				element: '#sharetabs',
				popover: {
					title: 'Proceed to map',
					description: "When you're ready, proceed to the map view to select your allocation method"
				}
			}
		]
	});

	onMount(() => {
		tour.useLocalStorage();
		if ($tour.completed === false) {
			console.log($tour);
			driverObj.drive();
			tour.set({ completed: true });
		}
	});

	// TODO generalize to colormap component or named after the series it used for
	const ipcc_green = '#A9C810';
	const ipcc_red = '#c82f10';
	const ipcc_blue = '#5bb0c6';
	const ipcc_purple = '#a67ab8';

	async function updateQueryParam(name: string, value: string) {
		if (browser) {
			const current = page.url.search;
			const params = new URLSearchParams(current);
			if (params.get(name) !== value) {
				params.set(name, value);
				await goto(`?${params.toString()}`);
			}
		}
	}

	function toggleEmissionGap() {
		emissionGapHover = !emissionGapHover;
	}

	let evt = $state({});
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function hoverBuilder(tmpl: (row: any) => string) {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		return function (e: any) {
			const row = e.row;
			if (row === undefined) {
				return;
			}
			e.msg = tmpl(row);
			evt = e;
		};
	}
	const hoverhistoricalEmissions = hoverBuilder(
		(row) =>
			`The historical greenhouse gas emissions in ${row.time} were ${row.value.toFixed(1)} Gt CO₂e`
	);
	const hoverPathway = hoverBuilder(
		(row) =>
			`Your selected global pathway emission in ${row.time} is ${row.value.toFixed(1)} Gt CO₂e`
	);
	const hoverCurrentPolicy = hoverBuilder(
		(row) => `Current policy scenarios in ${row.time} is on average ${row.mean.toFixed(1)} Gt CO₂e`
	);
	const hoverNdc = hoverBuilder(
		(row) => `NDCs in ${row.time} is on average ${row.mean.toFixed(1)} Gt CO₂e`
	);
	const hoverNetzero = hoverBuilder(
		(row) => `Net zero-scenarios in ${row.time} is on average ${row.mean.toFixed(1)} Gt CO₂e`
	);
	// When series overlap the top most series will react to mouse events

	let policyPathwayToggles = $state({
		current: false,
		ndc: false,
		netzero: false
	});

	let ambitionGapHover = $state(false);
	let emissionGapHover = $state(false);

	// $: console.log(data.result.currentPolicy); // only nans in input data...
	// Transitions
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const pathwayCarbonTweened = tweened(data.result.pathway, tweenOptions);
	run(() => {
		pathwayCarbonTweened.set(data.result.pathway);
	});
</script>

<div class="flex h-full gap-4">
	<Sidebar>
		<GlobalBudgetCard
			remaining={data.result.budget.remaining}
			relative={data.result.budget.relative}
		/>
		<div id="globalquerycard">
			<GlobalQueryCard
				options={data.pathway.options}
				query={data.pathway.query}
				onChange={updateQueryParam}
			/>
		</div>
		<div id="references">
			<div class="card card-compact min-w-full bg-base-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">Reference pathways</h2>
					<p>
						Use the checkboxes below to compare your pathway with common references. Of particular
						interest is the
						<span
							class="tooltip cursor-pointer"
							role="tooltip"
							onmouseenter={toggleEmissionGap}
							onmouseleave={toggleEmissionGap}
							data-tip="The implementation gap is the difference between your scenario and current policy projections."
							>implementation ⓘ</span
						>
						<!-- and # TODO: removed NDC gap because showing wrong part (see Annual NZ Report) see issue #107
						<span
							class="tooltip cursor-pointer"
							role="tooltip"
							on:mouseenter={toggleAmbitionGap}
							on:mouseleave={toggleAmbitionGap}
							data-tip="The NDC gap is the
				difference between current policy projections and projections of current NDC pledges.">NDC ⓘ</span
						> -->
						gap.
					</p>
					<ul class="">
						<li>
							<label class="cursor-pointer">
								<input
									type="checkbox"
									style={`background-color: ${ipcc_green}`}
									class="m-1 scale-125 shadow"
									checked
									disabled
								/>{' '}Your pathway</label
							>
						</li>
						<li>
							<label class="cursor-pointer">
								<input
									type="checkbox"
									style={`background-color: ${ipcc_red}`}
									class="m-1 scale-125 shadow"
									bind:checked={policyPathwayToggles.current}
								/>{' '}Projections of current policies</label
							>
						</li>
						<li>
							<label class="cursor-pointer">
								<input
									type="checkbox"
									style={`background-color: ${ipcc_purple}`}
									class="m-1 scale-125 shadow"
									bind:checked={policyPathwayToggles.ndc}
								/>{' '}Projections of nationally determined contributions (NDCs)</label
							>
						</li>
						<li>
							<label class="cursor-pointer">
								<input
									type="checkbox"
									style={`background-color: ${ipcc_blue}`}
									class="m-1 scale-125 shadow"
									bind:checked={policyPathwayToggles.netzero}
								/>{' '}Projections of net-zero pledges</label
							>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</Sidebar>
	<div class="flex grow flex-col">
		<div id="sharetabs">
			<ShareTabs />
		</div>
		<div class="relative grow bg-base-100 p-4 shadow-lg">
			<Pathway {evt} yAxisTtle="Greenhouse gas emissions (Gt CO₂e/year)">
				<Line
					data={data.result.historicalEmissions}
					x={'time'}
					y={'value'}
					color="black"
					mouseover={hoverhistoricalEmissions}
					mouseout={(e) => (evt = e)}
				/>
				{#if policyPathwayToggles.current || emissionGapHover}
					<Line data={data.result.currentPolicy} x={'time'} y={'mean'} color={ipcc_red} />
					<Area
						data={data.result.currentPolicy}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={ipcc_red}
						mouseover={hoverCurrentPolicy}
						mouseout={(e) => (evt = e)}
					/>
				{/if}
				{#if policyPathwayToggles.ndc || ambitionGapHover}
					<Line data={data.result.ndc} x={'time'} y={'mean'} color={ipcc_purple} />
					<Area
						data={data.result.ndc}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={ipcc_purple}
						mouseover={hoverNdc}
						mouseout={(e) => (evt = e)}
					/>
				{/if}
				{#if policyPathwayToggles.netzero}
					<Line data={data.result.netzero} x={'time'} y={'mean'} color={ipcc_blue} />
					<Area
						data={data.result.netzero}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={ipcc_blue}
						mouseover={hoverNetzero}
						mouseout={(e) => (evt = e)}
					/>
				{/if}

				{#if ambitionGapHover}
					<Gap x={data.result.gap.index} y0={data.result.gap.ndc} y1={data.result.gap.budget} />
				{/if}
				{#if emissionGapHover}
					<Gap x={data.result.gap.index} y0={data.result.gap.curPol} y1={data.result.gap.budget} />
				{/if}

				<Line
					data={$pathwayCarbonTweened}
					x={'time'}
					y={'value'}
					color={ipcc_green}
					mouseover={hoverPathway}
					mouseout={(e) => (evt = e)}
				/>
			</Pathway>
		</div>
	</div>
</div>
