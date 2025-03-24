<script lang="ts">
	import { page } from '$app/stores';
	import type { Region } from './api';
	interface Props {
		info: Region;
		regionsOfCountry?: Region[];
		countriesOfRegion?: Region[];
	}

	let { info, countriesOfRegion, regionsOfCountry }: Props = $props();

	console.log(countriesOfRegion);
	const blankFlag =
		'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480"%3E%3C/svg%3E';
	let regionFlag = $state(`https://flagcdn.com/${info.iso2?.toLowerCase()}.svg`);
</script>

<div id="country-header" class="flex flex-row items-center gap-4 pb-2">
	<a href={`/map${$page.url.search}`} title="Back to map" aria-label="Back to map">
		<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 256 256"
			><path
				fill="currentColor"
				d="M128 20a108 108 0 1 0 108 108A108.12 108.12 0 0 0 128 20Zm0 192a84 84 0 1 1 84-84a84.09 84.09 0 0 1-84 84Zm52-84a12 12 0 0 1-12 12h-51l11.52 11.51a12 12 0 0 1-17 17l-32-32a12 12 0 0 1 0-17l32-32a12 12 0 0 1 17 17L117 116h51a12 12 0 0 1 12 12Z"
			/></svg
		>
	</a>
	<img
		src={regionFlag}
		class="h-8"
		alt={info.name}
		onerror={() => {
			regionFlag = blankFlag;
		}}
	/>
	<h1 class="text-3xl font-bold">{info.name}</h1>
	{#if countriesOfRegion}
		<div class="flex flex-row gap-2">
			{#each countriesOfRegion as country}
				<a
					href={`/regions/${country.iso3}`}
					title={`View ${country.name}`}
					aria-label={`View ${country.name}`}
				>
					<img
						src={`https://flagcdn.com/${country.iso2?.toLowerCase()}.svg`}
						alt={country.name}
						class="h-4"
						onerror={() => {
							regionFlag = blankFlag;
						}}
					/>
				</a>
			{/each}
		</div>
	{/if}
	{#if regionsOfCountry}
		<div class="flex flex-row gap-2">
			{#each regionsOfCountry as region}
				<a
					href={`/regions/${region.iso3}`}
					title={`View ${region.name}`}
					aria-label={`View ${region.name}`}
				>
					<img
						src={`https://flagcdn.com/${region.iso2?.toLowerCase()}.svg`}
						alt={region.name}
						class="h-4"
						onerror={() => {
							regionFlag = blankFlag;
						}}
					/>
				</a>
			{/each}
		</div>
	{/if}
</div>
