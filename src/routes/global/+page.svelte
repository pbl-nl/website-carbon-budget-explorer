<script lang="ts">
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';

	import ShareTabs from '$lib/ShareTabs.svelte';
	import Pathway from '$lib/charts/Pathway.svelte';
	import Line from '$lib/charts/components/Line.svelte';
	import Area from '$lib/charts/components/Area.svelte';
	import Gap from '$lib/charts/components/Gap.svelte';

	import type { PageData } from '../global/$types';
	import GlobalBudgetCard from '$lib/GlobalBudgetCard.svelte';
	import GlobalQueryCard from '$lib/GlobalQueryCard.svelte';
	import type { ComponentEvents, SvelteComponent } from 'svelte';

	export let data: PageData;

	// TODO generalize to colormap component or named after the series it used for
	const ipcc_green = '#82a56e';
	const ipcc_red = '#f5331e';
	const ipcc_blue = '#5bb0c6';
	const ipcc_purple = '#a67ab8';

	function updateQueryParam(name: string, value: string) {
		if (browser) {
			const params = new URLSearchParams($page.url.search);
			params.set(name, value);
			goto(`?${params.toString()}`);
		}
	}

	function toggleAmbitionGap() {
		ambitionGapHover = !ambitionGapHover;
	}
	function toggleEmissionGap() {
		emissionGapHover = !emissionGapHover;
	}

	let evt = {};
	function hoverBuilder(tmpl: (row: any) => string) {
		return function (e: ComponentEvents<SvelteComponent>) {
			const row = e.detail.row;
			if (row === undefined) {
				return;
			}
			e.detail.msg = tmpl(row);
			evt = e;
		};
	}
	const hoverHistoricalCarbon = hoverBuilder(
		(row) => `Historical emission in ${row.time} was ${row.value.toFixed(0)} Gt CO₂e`
	);
	const hoverPathway = hoverBuilder(
		(row) =>
			`Your selected global pathway emission in ${row.time} is on average ${row.mean.toFixed(
				0
			)} Gt CO₂e`
	);
	const hoverCurrentPolicy = hoverBuilder(
		(row) => `Current policy in ${row.time} is on average ${row.mean.toFixed(0)} Gt CO₂e`
	);
	const hoverNdc = hoverBuilder(
		(row) => `NDCs in ${row.time} is on average ${row.mean.toFixed(0)} Gt CO₂e`
	);
	const hoverNetzero = hoverBuilder(
		(row) => `Net zero-scenarios in ${row.time} is on average ${row.mean.toFixed(0)} Gt CO₂e`
	);
	// When series overlap the top most series will react to mouse events

	let policyPathwayToggles = {
		current: false,
		ndc: false,
		netzero: false
	};

	let ambitionGapHover = false;
	let emissionGapHover = false;

	// $: console.log(data.result.currentPolicy); // only nans in input data...
	// Transitions
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const pathwayCarbonTweened = tweened(data.result.pathwayCarbon, tweenOptions);
	$: pathwayCarbonTweened.set(data.result.pathwayCarbon);
	const emissionGapTweened = tweened(data.result.stats.gaps.emission, tweenOptions);
	$: emissionGapTweened.set(data.result.stats.gaps.emission);
	const ambitionGapTweened = tweened(data.result.stats.gaps.ambition, tweenOptions);
	$: ambitionGapTweened.set(data.result.stats.gaps.ambition);
</script>

<div class="flex gap-4">
	<div id="sidebar" class="flex h-full max-w-[25%] flex-col justify-between gap-4">
		<GlobalBudgetCard total={data.result.stats.total} remaining={data.result.stats.remaining} />
		<GlobalQueryCard
			choices={data.pathway.choices}
			query={data.pathway.query}
			onChange={updateQueryParam}
		/>
		<div class="card-compact card prose bg-base-100 shadow-xl">
			<div class="card-body">
				<h2 class="not-prose card-title">Reference pathways</h2>
				<p>Compare your pathway to the following reference pathways:</p>
				<ul class="not-prose">
					<li>
						<label>
							<b style={`color: ${ipcc_red}`}>▬</b>
							<input type="checkbox" bind:checked={policyPathwayToggles.current} />{' '}Current
							policy</label
						>
					</li>
					<li>
						<label>
							<b style={`color: ${ipcc_blue}`}>▬</b>
							<input type="checkbox" bind:checked={policyPathwayToggles.ndc} />{' '}Nationally
							determined contributions (NDCs)</label
						>
					</li>
					<li>
						<label>
							<b style={`color: ${ipcc_purple}`}>▬</b>
							<input type="checkbox" bind:checked={policyPathwayToggles.netzero} />{' '}Net
							zero-scenarios</label
						>
					</li>
				</ul>
				<p>
					The difference between your pathway and the reference pathways is characterized by the <span
						class="tooltip"
						role="tooltip"
						on:mouseenter={toggleEmissionGap}
						on:mouseleave={toggleEmissionGap}
						data-tip="The emission gap is the difference between your scenario and the current policy."
						>emission 🛈</span
					>
					and
					<span
						class="tooltip"
						role="tooltip"
						on:mouseenter={toggleAmbitionGap}
						on:mouseleave={toggleAmbitionGap}
						data-tip="The ambition gap is the
				difference between your scenario and the NDCs.">ambition 🛈</span
					>
					gaps.
				</p>
			</div>
		</div>
		<div class="stats shadow-xl">
			<div class="stat tooltip place-items-center">
				<div class="stat-title">Emission gap in 2030</div>
				<div class="stat-value">{$emissionGapTweened.toFixed(0)}</div>
				<div class="stat-desc" title="Gigaton carbon dioxide equivalent">Gt CO₂e</div>
			</div>

			<div class="stat place-items-center">
				<div class="stat-title">Ambition gap in 2030</div>
				<div class="stat-value">{$ambitionGapTweened.toFixed(0)}</div>
				<div class="stat-desc" title="Gigaton carbon dioxide equivalent">Gt CO₂e</div>
				<p class="text-xs" />
			</div>
		</div>
	</div>

	<div class="flex grow flex-col">
		<ShareTabs />
		<div class="relative grow bg-base-100 p-4 shadow-lg">
			<Pathway {evt} yAxisTtle="Greenhouse gas emissions (Gt CO₂e/year)">
				<Line
					data={data.result.historicalCarbon}
					x={'time'}
					y={'value'}
					color="black"
					on:mouseover={hoverHistoricalCarbon}
					on:mouseout={(e) => (evt = e)}
				/>
				{#if policyPathwayToggles.current || emissionGapHover}
					<Line data={data.result.currentPolicy} x={'time'} y={'mean'} color={ipcc_red} />
					<Area
						data={data.result.currentPolicy}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={ipcc_red}
						on:mouseover={hoverCurrentPolicy}
						on:mouseout={(e) => (evt = e)}
					/>
				{/if}
				{#if policyPathwayToggles.ndc || ambitionGapHover}
					<Line data={data.result.ndc} x={'time'} y={'mean'} color={ipcc_blue} />
					<Area
						data={data.result.ndc}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={ipcc_blue}
						on:mouseover={hoverNdc}
						on:mouseout={(e) => (evt = e)}
					/>
				{/if}
				{#if policyPathwayToggles.netzero}
					<Line data={data.result.netzero} x={'time'} y={'mean'} color={ipcc_purple} />
					<Area
						data={data.result.netzero}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={ipcc_purple}
						on:mouseover={hoverNetzero}
						on:mouseout={(e) => (evt = e)}
					/>
				{/if}

				{#if ambitionGapHover}
					<Gap
						x={data.result.stats.gaps.index}
						y0={data.result.stats.gaps.ndc}
						y1={data.result.stats.gaps.budget}
					/>
				{/if}
				{#if emissionGapHover}
					<Gap
						x={data.result.stats.gaps.index}
						y0={data.result.stats.gaps.curPol}
						y1={data.result.stats.gaps.budget}
					/>
				{/if}

				<Line data={$pathwayCarbonTweened} x={'time'} y={'mean'} color={ipcc_green} />
				<Area
					data={$pathwayCarbonTweened}
					x={'time'}
					y0={'min'}
					y1={'max'}
					color={ipcc_green}
					on:mouseover={hoverPathway}
					on:mouseout={(e) => (evt = e)}
				/>
			</Pathway>
		</div>
	</div>
</div>
