<script lang="ts">
	import CountryHeader from '$lib/CountryHeader.svelte';

	import PrincipleStatsTable from '$lib/PrincipleStatsTable.svelte';

	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import type { PageData } from './$types';
	import Pathway from '$lib/charts/Pathway.svelte';
	import Line from '$lib/charts/components/Line.svelte';
	import Area from '$lib/charts/components/Area.svelte';
	import { principles } from '$lib/principles';
	import { cubicOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';
	import MiniPathwayCard from '$lib/MiniPathwayCard.svelte';
	import GlobalBudgetCard from '$lib/GlobalBudgetCard.svelte';
	import GlobalQueryCard from '$lib/GlobalQueryCard.svelte';
	import type { ComponentEvents, SvelteComponent } from 'svelte';
	import NdcRange from '$lib/charts/components/NdcRange.svelte';
	import Sidebar from '$lib/Sidebar.svelte';

	export let data: PageData;

	function updateQueryParam(name: string, value: string) {
		if (browser) {
			const params = new URLSearchParams($page.url.search);
			params.set(name, value);
			goto(`?${params.toString()}`);
		}
	}

	let activeEffortSharings = Object.fromEntries(
		Object.keys(principles).map((id) => [id, id === data.initialEffortSharingName])
	);

	// Transitions
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedEffortSharing = tweened(data.effortSharing, tweenOptions);
	$: tweenedEffortSharing.set(data.effortSharing);

	// Hover effort sharing
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
		(row) => `Historical emissions in ${row.time} were ${row.value.toFixed(0)} Mt CO₂e`
	);
	const hoverNdc = hoverBuilder(
		(row) =>
			`Nationally determined contribution in ${row.time} ranges from ${row.max.toFixed(
				0
			)} to ${row.min.toFixed(0)} Mt CO₂e`
	);

	function hoverEffortSharing(id: string) {
		return hoverBuilder(
			(row) => `${id} in ${row.time} is ${row.mean.toFixed(0)} Mt CO₂e (with default settings)`
		);
	}

	const euMemberStates = [
		'AUT',
		'BEL',
		'BGR',
		'HRV',
		'CYP',
		'CZE',
		'DNK',
		'EST',
		'FIN',
		'FRA',
		'DEU',
		'GRC',
		'HUN',
		'IRL',
		'ITA',
		'LVA',
		'LTU',
		'LUX',
		'MLT',
		'NLD',
		'POL',
		'PRT',
		'ROU',
		'SVK',
		'SVN',
		'ESP',
		'SWE'
	];

	// Function to check if the region is an EU member state
	function isEuMemberState(region: string) {
		return euMemberStates.includes(region);
	}
</script>

<div class="flex h-full flex-row gap-4">
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
		<MiniPathwayCard global={data.global} />
	</Sidebar>
	<div class="flex h-full grow flex-col">
		<!-- setting *any* initial height + grow fixes overflow-auto with h-full -->
		<div class="flex h-[100px] grow flex-col overflow-y-auto rounded-md bg-base-100 p-2 shadow-xl">
			<CountryHeader info={data.info} />
			<section id="key-indicators">
				<div class="px-12">
					<p>
						<span class="font-bold"> NDC ambition in 2030 relative to 2015: </span>
						<span>
							{#if data.indicators.ndcAmbition === null}
								-
							{:else if data.indicators.ndcAmbition.min === data.indicators.ndcAmbition.max}
								{#if isEuMemberState(data.info.iso3)}
									EU Member States do not have individual NDCs. The EU27's joint NDC target is to
									reduce GHG emissions by at least 55% by 2030 compared to 1990 levels. This
									translates to 2085 Mt CO₂e in 2030.
								{:else if data.indicators.ndcAmbition.min < 0}
									{Math.abs(data.indicators.ndcAmbition.min.toFixed(0))} % increase
								{:else}
									{data.indicators.ndcAmbition.min.toFixed(0)} % reduction
								{/if}
							{:else if isEuMemberState(data.info.iso3)}
								EU Member States do not have individual NDCs. The EU27's joint NDC target is to
								reduce GHG emissions by at least 55% by 2030 compared to 1990 levels. This
								translates to 2085 Mt CO₂e in 2030.
							{:else if data.indicators.ndcAmbition.min < 0 && data.indicators.ndcAmbition.max < 0}
								{`${Math.abs(data.indicators.ndcAmbition.max.toFixed(0))} - ${Math.abs(
									data.indicators.ndcAmbition.min.toFixed(0)
								)} % increase`}
							{:else}
								{`${data.indicators.ndcAmbition.min.toFixed(
									0
								)} - ${data.indicators.ndcAmbition.max.toFixed(0)} % reduction`}
							{/if}
						</span>
					</p>
				</div>
			</section>

			<PrincipleStatsTable reductions={data.reductions} bind:activeEffortSharings />
			<section id="overview" class="grow">
				<!-- TODO compute smarter extent -->
				<Pathway
					yDomain={[data.historicalCarbon.extent[1] * -0.3, data.historicalCarbon.extent[1] * 1.5]}
					{evt}
					yAxisTtle="GHG emissions (Mt CO₂e/year)"
				>
					<Line
						data={data.historicalCarbon.data.filter((d) => d.time >= 1990)}
						x={'time'}
						y={'value'}
						color="black"
						on:mouseover={hoverHistoricalCarbon}
						on:mouseout={(e) => (evt = e)}
					/>
					{#each Object.entries(principles) as [id, { color, label }]}
						{#if activeEffortSharings[id]}
							<g name={id}>
								<Line data={$tweenedEffortSharing[id]} x={'time'} y={'mean'} {color} />
								<Area
									data={$tweenedEffortSharing[id]}
									x={'time'}
									y0={'min'}
									y1={'max'}
									{color}
									on:mouseover={hoverEffortSharing(label)}
									on:mouseout={(e) => (evt = e)}
								/>
							</g>
						{/if}
					{/each}
					{#if !isEuMemberState(data.info.iso3)}
						{#each Object.entries(data.indicators.ndc_inventory) as [year, range]}
							<NdcRange
								x={parseInt(year)}
								y0={range[0]}
								y1={range[1]}
								textNdcMin={`Min: ${range[0].toFixed(0)}`}
								textNdcMax={`Max: ${range[1].toFixed(0)}`}
								textNdc={`NDC`}
								color="black"
								on:mouseover={hoverNdc}
								on:mouseout={(e) => (evt = e)}
							/>
						{/each}
						<!-- {#each Object.entries(data.indicators.ndc_jones) as [year, range]}
							<NdcRange
								x={parseInt(year)}
								y0={range[0]}
								y1={range[1]}
								textNdcMin={` `}
								textNdcMax={` `}
								textNdc={` `}
								color="gray"
								on:mouseover={hoverNdc}
								on:mouseout={(e) => (evt = e)}
							/>
						{/each} -->
					{/if}
				</Pathway>
			</section>
		</div>
	</div>
</div>
