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
			`Nationally determined contribution at ${row.time} ranges from ${row.max.toFixed(
				0
			)} to ${row.min.toFixed(0)} Mt CO₂e`
	);

	function hoverEffortSharing(id: string) {
		return hoverBuilder(
			(row) => `${id} in ${row.time} is on average ${row.mean.toFixed(0)} Mt CO₂e`
		);
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
						<span class="font-bold"> Historical emissions: </span>
						<span>
							{(data.indicators.historicalCarbon / 1_000).toFixed()}
							Gt CO₂e
						</span>
					</p>
					<p>
						<span class="font-bold"> NDC ambition in 2030 relative to 1990: </span><span
							>{data.indicators.ndcAmbition === null
								? '-'
								: data.indicators.ndcAmbition.toFixed(0)}<span
								class="tooltip cursor-pointer"
								role="tooltip"
								data-tip="In terms of greenhouse gases without taking into account land use, land use change and forestry (LULUCF)."
								>% reduction ⓘ</span
							>
						</span>
					</p>
				</div>
			</section>

			<PrincipleStatsTable reductions={data.reductions} bind:activeEffortSharings />
			<section id="overview" class="grow">
				<!-- TODO compute smarter extent -->
				<Pathway
					yDomain={[data.historicalCarbon.extent[1] * -0.2, data.historicalCarbon.extent[1]]}
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
					{#each Object.entries(data.indicators.ndc) as [year, range]}
						<NdcRange
							x={parseInt(year)}
							y0={range[0]}
							y1={range[1]}
							on:mouseover={hoverNdc}
							on:mouseout={(e) => (evt = e)}
						/>
					{/each}
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
				</Pathway>
			</section>
		</div>
	</div>
</div>
