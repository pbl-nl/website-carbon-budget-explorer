<script lang="ts">
	import { run } from 'svelte/legacy';

	import CountryHeader from '$lib/CountryHeader.svelte';

	import StatsTable from '$lib/StatsTable.svelte';

	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import type { PageData } from './$types';
	import Pathway from '$lib/charts/Pathway.svelte';
	import Line from '$lib/charts/components/Line.svelte';
	import Area from '$lib/charts/components/Area.svelte';
	import { allocationMethods } from '$lib/allocationMethods';
	import { cubicOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';
	import MiniPathwayCard from '$lib/MiniPathwayCard.svelte';
	import GlobalBudgetCard from '$lib/GlobalBudgetCard.svelte';
	import GlobalQueryCard from '$lib/GlobalQueryCard.svelte';
	import type { ComponentEvents, SvelteComponent } from 'svelte';
	import NdcRange from '$lib/charts/components/NdcRange.svelte';
	import Sidebar from '$lib/Sidebar.svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	function updateQueryParam(name: string, value: string) {
		if (browser) {
			const params = new URLSearchParams($page.url.search);
			if (params.get(name) !== value) {
				params.set(name, value);
				goto(`?${params.toString()}`);
			}
		}
	}

	// Not all regions have data for all allocation methods
	let availableAllocationMethods = $derived(new Set(Object.keys(data.allocationMethod)));

	let activeAllocationMethods = $state(
		Object.fromEntries(
			Object.keys(allocationMethods)
				.filter((p) => availableAllocationMethods.has(p))
				.map((id) => [id, id === data.initialAllocationMethod])
		)
	);

	// Transitions
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedAllocationMethod = tweened(data.allocationMethod, tweenOptions);
	run(() => {
		tweenedAllocationMethod.set(data.allocationMethod);
	});

	// Hover effort sharing
	let evt = $state({});
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function hoverBuilder(tmpl: (row: any) => string) {
		return function (e: ComponentEvents<SvelteComponent>) {
			const row = e.row;
			if (row === undefined) {
				return;
			}
			e.msg = tmpl(row);
			evt = e;
		};
	}
	const hoverhistoricalEmissions = hoverBuilder(
		(row) => `Historical emissions in ${row.time} were ${row.value.toFixed(0)} Mt CO₂e`
	);
	const hoverNdc = hoverBuilder(
		(row) =>
			`Nationally determined contribution in ${row.time} ranges from ${row.max.toFixed(
				0
			)} to ${row.min.toFixed(0)} Mt CO₂e`
	);

	function hoverAllocationMethod(id: string) {
		return hoverBuilder(
			(row) => `${id} in ${row.time} is ${row.mean.toFixed(0)} Mt CO₂e (with default settings)`
		);
	}

	let domainExtent = $derived.by(() => {
		const extent: [number, number] = [-100, 100];
		if (data.historicalEmissions.extent[1] !== undefined) {
			extent[0] = data.historicalEmissions.extent[1] * -0.3;
			extent[1] = data.historicalEmissions.extent[1] * 1.5;
		} else {
			// If there is no historical data, use all effort sharing data
			const allocationMethods = Object.values(data.allocationMethod).flatMap((d) => d);
			if (allocationMethods.length > 0) {
				extent[0] = Math.min(...allocationMethods.map((d) => d.min));
				extent[1] = Math.max(...allocationMethods.map((d) => d.max));
			}
		}
		return extent;
	});
</script>

<div class="flex h-full flex-row gap-4">
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
		<MiniPathwayCard global={data.global} />
	</Sidebar>
	<div class="flex h-full grow flex-col">
		<!-- setting *any* initial height + grow fixes overflow-auto with h-full -->
		<div class="flex h-[100px] grow flex-col overflow-y-auto rounded-md bg-base-100 p-2 shadow-xl">
			<CountryHeader
				info={data.info}
				regionsOfCountry={data.regionsOfCountry}
				countriesOfRegion={data.countriesOfRegion}
			/>
			<section id="key-indicators">
				<div class="px-12">
					<p>
						<span class="font-bold"> NDC ambition in 2030 relative to 2015: </span>
						<span>
							{#if data.ndcReduction === null}
								-
							{:else if data.ndcReduction.min === data.ndcReduction.max}
								{#if data.isEuMemberState}
									EU Member States do not have individual NDCs. The EU27's joint NDC target is to
									reduce GHG emissions by at least 55% by 2030 compared to 1990 levels. This
									translates to 2085 Mt CO₂e in 2030.
								{:else if data.ndcReduction.min < 0}
									{Math.abs(data.ndcReduction.min).toFixed(0)} % increase
								{:else}
									{data.ndcReduction.min.toFixed(0)} % reduction
								{/if}
							{:else if data.isEuMemberState}
								EU Member States do not have individual NDCs. The EU27's joint NDC target is to
								reduce GHG emissions by at least 55% by 2030 compared to 1990 levels. This
								translates to 2085 Mt CO₂e in 2030.
							{:else if data.ndcReduction.min < 0 && data.ndcReduction.max < 0}
								{`${Math.abs(data.ndcReduction.max).toFixed(0)} - ${Math.abs(
									data.ndcReduction.min
								).toFixed(0)} % increase`}
							{:else}
								{`${data.ndcReduction.min.toFixed(
									0
								)} - ${data.ndcReduction.max.toFixed(0)} % reduction`}
							{/if}
						</span>
					</p>
				</div>
			</section>

			<StatsTable
				reductions={data.reductions}
				bind:activeAllocationMethods
				{availableAllocationMethods}
			/>
			<section id="overview" class="grow">
				<Pathway yDomain={domainExtent} {evt} yAxisTtle="GHG emissions (Mt CO₂e/year)">
					<Line
						data={data.historicalEmissions.data.filter((d) => d.time >= 1990)}
						x={'time'}
						y={'value'}
						color="black"
						mouseover={hoverhistoricalEmissions}
						mouseout={(e) => (evt = e)}
					/>
					{#each Object.entries(allocationMethods) as [id, { color, label }]}
						{#if activeAllocationMethods[id]}
							<g name={id}>
								<Line
									data={$tweenedAllocationMethod[id]}
									x={'time'}
									y={'mean'}
									{color}
									mouseover={hoverAllocationMethod(label)}
									mouseout={(e) => (evt = e)}
								/>
								<Area
									data={$tweenedAllocationMethod[id]}
									x={'time'}
									y0={'min'}
									y1={'max'}
									{color}
									mouseover={hoverAllocationMethod(label)}
									mouseout={(e) => (evt = e)}
								/>
							</g>
						{/if}
					{/each}
					{#if !data.isEuMemberState && data.ndcProjection.ndc_inventory !== null}
						{#each Object.entries(data.ndcProjection.ndc_inventory) as [year, range]}
							<NdcRange
								x={parseInt(year)}
								y0={range[0]}
								y1={range[1]}
								textNdcMin={`Min: ${range[0].toFixed(0)}`}
								textNdcMax={`Max: ${range[1].toFixed(0)}`}
								textNdc={`NDC`}
								color="black"
								mouseover={hoverNdc}
								mouseout={(e) => (evt = e)}
							/>
						{/each}
						<!-- {#each Object.entries(data.ndcProjection.ndc_jones) as [year, range]}
							<NdcRange
								x={parseInt(year)}
								y0={range[0]}
								y1={range[1]}
								textNdcMin={` `}
								textNdcMax={` `}
								textNdc={` `}
								color="gray"
								mouseover={hoverNdc}
								mouseout={(e) => (evt = e)}
							/>
						{/each} -->
					{/if}
				</Pathway>
			</section>
		</div>
	</div>
</div>
