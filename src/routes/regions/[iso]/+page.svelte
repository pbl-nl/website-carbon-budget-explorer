<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import GlobalBudgetForm from '$lib/PathwayForm.svelte';

	import type { PageData } from './$types';
	import Pathway from '$lib/charts/Pathway.svelte';
	import Line from '$lib/charts/components/Line.svelte';
	import Area from '$lib/charts/components/Area.svelte';
	import { principles } from '$lib/principles';
	import Gap from '$lib/charts/components/Gap.svelte';
	import { cubicOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';
	export let data: PageData;

	function updateQueryParam(name: string, value: string) {
		if (browser) {
			const params = new URLSearchParams($page.url.search);
			params.set(name, value);
			goto(`?${params.toString()}`);
		}
	}
	// Bottom colors from https://colorbrewer2.org/#type=qualitative&scheme=Pastel1&n=9
	const referenceColors = {
		currentPolicy: '#e5d8bd',
		ndc: '#fddaec',
		netzero: '#f2f2f2' // TODO find better color, now almost same as background
	};

	let activeEffortSharings = Object.fromEntries(
		Object.keys(principles).map((id) => [id, id === data.initialEffortSharingName])
	);

	let activeReference: string[] = [];

	// Gap hover
	let gapIndex = data.reference.ndc.map((d) => d.time).indexOf(2030);
	let hoveredAmbitionGap: string | null = null;
	let hoveredEmissionGap: string | null = null;

	// Transitions
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedEffortSharing = tweened(data.effortSharing, tweenOptions);
	$: tweenedEffortSharing.set(data.effortSharing);
</script>

<main class="flex flex-col gap-2">
	<section id="key-indicators">
		<div class="border-10 mb-2 flex flex-row gap-10 p-2">
			<div class="grow">
				<header class="flex flex-row gap-4">
					<img
						src={`https://flagcdn.com/${data.info.iso2?.toLowerCase()}.svg`}
						class="h-8"
						alt={data.info.name}
					/>
					<h1 class="text-3xl font-bold">{data.info.name}</h1>
				</header>
				<p class="text-2xl">Key indicators</p>
				<div class="justify-left flex flex-col gap-4">
					<div class="">
						<p>NDC Ambition (normalized)</p>
						<p>{data.indicators.ndcAmbition}</p>
					</div>
					<div class="">
						<p>Historical emissions (cumulative)</p>
						<p>{(data.indicators.historicalCarbon / 1_000).toFixed()} Gt CO₂</p>
					</div>
				</div>
			</div>
			{#each Object.entries(principles) as [id, { label, color }]}
				<button on:click={() => (activeEffortSharings[id] = !activeEffortSharings[id])}>
					<div
						class={activeEffortSharings[id]
							? 'relative h-48 w-48 border-4 text-start shadow-lg'
							: 'relative h-48 w-48 border-4 text-start shadow-lg'}
						style={`border-color: ${activeEffortSharings[id] ? color : '#EEE'}`}
					>
						<h3 class="h-1/3 px-2 text-xl" style={`background-color: ${color}`}>
							{label}
							<a title="More information" target="_blank" rel="noopener" href={`/about#${id}`}>ⓘ</a>
						</h3>
						<div class="p-2">
							<p>Ambition gap:</p>
							<p
								on:mouseenter={() => (hoveredAmbitionGap = id)}
								on:mouseleave={() => (hoveredAmbitionGap = null)}
								class="inline hover:bg-[#888] hover:bg-opacity-50"
							>
								{$tweenedEffortSharing[id].ambitionGap.toFixed(2)} Mt CO2
							</p>
							<p>Emission gap:</p>
							<p
								on:mouseenter={() => (hoveredEmissionGap = id)}
								on:mouseleave={() => (hoveredEmissionGap = null)}
								class="inline hover:bg-[#888] hover:bg-opacity-50"
							>
								{$tweenedEffortSharing[id].emissionGap.toFixed(2)} Mt CO2
							</p>
						</div>
					</div>
				</button>
			{/each}
		</div>
	</section>
	<hr class="pb-2" />
	<section id="overview" class="flex h-[500px] grow flex-row">
		<div>
			<GlobalBudgetForm
				choices={data.pathway.choices}
				query={data.pathway.query}
				onChange={updateQueryParam}
			/>
			<div>
				<h1 class="pt-4">Reference pathways</h1>
				<div>
					<!-- TODO this checkbox group is also used in /global page, deduplicate -->
					<label class="block">
						<b style={`color: ${referenceColors.currentPolicy}`}>▬</b>
						<input
							class="mr-1"
							type="checkbox"
							value="currentPolicy"
							bind:group={activeReference}
						/>
						Current policy</label
					>
					<label class="block">
						<b style={`color: ${referenceColors.ndc}`}>▬</b>
						<input class="mr-1" type="checkbox" value="ndc" bind:group={activeReference} />
						Nationally determined contributions (NDCs)
					</label>
					<label class="block">
						<b style={`color: ${referenceColors.netzero}`}>▬</b>
						<input class="mr-1" type="checkbox" value="netzero" bind:group={activeReference} />
						Net zero-scenarios
					</label>
				</div>
			</div>
		</div>

		<!-- TODO compute smarter extent -->
		<Pathway yDomain={[data.historicalCarbon.extent[1] * -0.2, data.historicalCarbon.extent[1]]}>
			<Line
				data={data.historicalCarbon.data.filter((d) => d.time >= 1990)}
				x={'time'}
				y={'value'}
				color="black"
			/>
			{#each Object.entries(principles) as [id, { color }]}
				{#if activeEffortSharings[id] || hoveredAmbitionGap === id || hoveredEmissionGap === id}
					<g name={id}>
						{#if id === 'ECPC'}
							<!-- TODO show ECPC as error bar on chart -->
							<Gap
								x={$tweenedEffortSharing[id].CO2[0].time}
								y0={$tweenedEffortSharing[id].CO2[0].min}
								y1={$tweenedEffortSharing[id].CO2[0].max}
							/>
						{:else}
							<Line data={$tweenedEffortSharing[id].CO2} x={'time'} y={'mean'} {color} />
							<Area data={$tweenedEffortSharing[id].CO2} x={'time'} y0={'min'} y1={'max'} {color} />
						{/if}
						{#if activeEffortSharings[id] && hoveredAmbitionGap}
							<Gap
								x={2030}
								y0={data.reference.ndc[gapIndex].mean}
								y1={$tweenedEffortSharing[hoveredAmbitionGap].CO2.find((d) => d.time === 2030)
									?.mean || 0}
							/>
						{/if}
						{#if activeEffortSharings[id] && hoveredEmissionGap}
							<Gap
								x={2030}
								y0={data.reference.currentPolicy[gapIndex].mean}
								y1={$tweenedEffortSharing[hoveredEmissionGap].CO2.find((d) => d.time === 2030)
									?.mean || 0}
							/>
						{/if}
					</g>
				{/if}
			{/each}

			{#if activeReference.includes('currentPolicy') || hoveredEmissionGap}
				<g name="currentPolicy">
					<Line
						data={data.reference.currentPolicy}
						x={'time'}
						y={'mean'}
						color={referenceColors.currentPolicy}
					/>
					<Area
						data={data.reference.currentPolicy}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={referenceColors.currentPolicy}
					/>
				</g>
			{/if}
			{#if activeReference.includes('ndc') || hoveredAmbitionGap}
				<g name="ndc">
					<Line data={data.reference.ndc} x={'time'} y={'mean'} color={referenceColors.ndc} />
					<Area
						data={data.reference.ndc}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={referenceColors.ndc}
					/>
				</g>
			{/if}
			{#if activeReference.includes('netzero')}
				<g name="netzero">
					<Line
						data={data.reference.netzero}
						x={'time'}
						y={'mean'}
						color={referenceColors.netzero}
					/>
					<Area
						data={data.reference.netzero}
						x={'time'}
						y0={'min'}
						y1={'max'}
						color={referenceColors.netzero}
					/>
				</g>
			{/if}
		</Pathway>
	</section>
	<section id="description" class="py-8">
		<p>Some text about country carbon budget and plans.</p>

		<p>Ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl eget.</p>
	</section>
	<section id="details">
		<!-- TODO use same x-axis for all charts? -->
		<div>
			<h2 class="text-xl" id="pop">Population</h2>
			<div class="h-64">
				<Pathway yDomain={data.details.population.extent} xDomain={[1940, 2100]}>
					<Line data={data.details.population.data} x={'time'} y={'value'} color="black" />
				</Pathway>
			</div>
		</div>
		<div>
			<h2 class="text-xl" id="gdp">Gross domestic product (GDP)</h2>
			<div class="h-64">
				<Pathway yDomain={data.details.gdp.extent} xDomain={[1940, 2100]}>
					<Line data={data.details.gdp.data} x={'time'} y={'value'} color="black" />
				</Pathway>
			</div>
		</div>
		<div>
			<h2 class="text-xl" id="hist-emis">Historical emissions</h2>
			<div class="h-64">
				<Pathway yDomain={data.historicalCarbon.extent} xDomain={[1850, 2021]}>
					<Line data={data.historicalCarbon.data} x={'time'} y={'value'} color="black" />
				</Pathway>
			</div>
			<p>in Mt CO₂</p>
		</div>
		<div>
			<h2 class="text-xl" id="hist-emis">policy costs ????</h2>
			<div class="h-64">
				Ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl eget.
			</div>
		</div>
	</section>
</main>
