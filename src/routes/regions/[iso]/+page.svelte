<script lang="ts">
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
	const tweenedReductions = tweened(data.reductions, tweenOptions);
	$: tweenedReductions.set(data.reductions);

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
		(row) => `Historical emission in ${row.time} was ${row.value.toFixed(0)} Gt CO₂e`
	);
	const hoverNdc = hoverBuilder(
		(row) =>
			`Nationally determined contribution at ${row.time} ranges from ${row.max.toFixed(
				0
			)} to ${row.min.toFixed(0)} Gt CO₂e`
	);

	function hoverEffortSharing(id: string) {
		return hoverBuilder(
			(row) => `${id} in ${row.time} is on average ${row.mean.toFixed(0)} Mt CO₂e`
		);
	}

	const blankFlag =
		'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480"%3E%3C/svg%3E';
	let regionFlag = `https://flagcdn.com/${data.info.iso2?.toLowerCase()}.svg`;
</script>

<div class="flex h-full flex-row gap-4">
	<div id="sidebar" class="flex h-full max-w-[25%] flex-col gap-4">
		<GlobalBudgetCard total={data.pathway.stats.total} remaining={data.pathway.stats.remaining} />
		<GlobalQueryCard
			choices={data.pathway.choices}
			query={data.pathway.query}
			onChange={updateQueryParam}
		/>
		<MiniPathwayCard global={data.global} />
	</div>
	<div class="flex h-full grow flex-col">
		<div id="country-header" class="flex flex-row items-center gap-4 pb-2">
			<a href={`/map${$page.url.search}`} title="Back to map"
				><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 256 256"
					><path
						fill="currentColor"
						d="M128 20a108 108 0 1 0 108 108A108.12 108.12 0 0 0 128 20Zm0 192a84 84 0 1 1 84-84a84.09 84.09 0 0 1-84 84Zm52-84a12 12 0 0 1-12 12h-51l11.52 11.51a12 12 0 0 1-17 17l-32-32a12 12 0 0 1 0-17l32-32a12 12 0 0 1 17 17L117 116h51a12 12 0 0 1 12 12Z"
					/></svg
				>
			</a>
			<img
				src={regionFlag}
				class="h-8"
				alt={data.info.name}
				on:error={() => {
					regionFlag = blankFlag;
				}}
			/>
			<h1 class="text-3xl font-bold">{data.info.name}</h1>
		</div>
		<!-- setting *any* initial height + grow fixes overflow-auto with h-full -->
		<div class="h-[500px] grow overflow-y-auto rounded-md bg-base-100 p-2 shadow-xl">
			<section id="key-indicators">
				<div class="border-10 stats mb-2 flex flex-row gap-10 p-2">
					<div class="stat place-items-center bg-accent shadow-lg">
						<div class="stat-title">NDC Ambition (2030)</div>
						<div class="stat-value">
							{data.indicators.ndcAmbition === null ? '-' : data.indicators.ndcAmbition.toFixed(0)}%
						</div>
						<div class="stat-desc" title="With respect to emissions in 1990">
							wrt 1990 emissions
						</div>
					</div>

					<div class="stat place-items-center bg-accent shadow-lg">
						<div class="stat-title">Historical emissions</div>
						<div class="stat-value">
							{(data.indicators.historicalCarbon / 1_000).toFixed()}
						</div>
						<div class="stat-desc" title="cumulative gigaton carbon dioxide equivalent">
							Gt CO₂e (cumulative)
						</div>
					</div>
				</div>
				<div class="border-10 mb-2 flex w-full flex-row flex-wrap items-stretch gap-4 p-2">
					{#each Object.entries(principles) as [id, { label, color }]}
						<div class="border-4 text-start shadow-lg" style={`border-color: ${color}`}>
							<h3 class="px-2 text-center text-lg" style={`background-color: ${color}`}>
								{label}
								<a title="More information" target="_blank" rel="noopener" href={`/about#${id}`}
									>ⓘ</a
								>
							</h3>
							<div class="stats shadow">
								<div class="stat place-items-center">
									<div class="stat-title">2030 reduction</div>
									<div class="stat-value text-3xl">
										{$tweenedReductions[id][2030] === null
											? '-'
											: $tweenedReductions[id][2030].toFixed(0)}%
									</div>
									<div class="stat-desc" title="With respect to emissions in 1990">
										wrt 1990 emissions
									</div>
								</div>
								<div class="stat place-items-center">
									<div class="stat-title">2040 reduction</div>
									<div class="stat-value text-3xl">
										{$tweenedReductions[id][2040] === null
											? '-'
											: $tweenedReductions[id][2040].toFixed(0)}%
									</div>
									<div class="stat-desc" title="With respect to emissions in 1990">
										wrt 1990 emissions
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</section>
			<hr class="py-2" />
			<section id="overview" class="relative h-[500px] grow">
				<div id="overview-legend" class="absolute bottom-8 left-16 z-10">
					<h1>Effort sharing principle</h1>
					<ul>
						{#each Object.entries(principles) as [id, { label, color }]}
							<li>
								<label>
									<b style={`color: ${color}`}>▬</b>
									<input type="checkbox" bind:checked={activeEffortSharings[id]} />
									{' '}{label}
								</label>
							</li>
						{/each}
					</ul>
				</div>

				<!-- TODO compute smarter extent -->
				<Pathway
					yDomain={[data.historicalCarbon.extent[1] * -0.2, data.historicalCarbon.extent[1]]}
					{evt}
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
