<script lang="ts">
	import { page } from '$app/stores';
	import type { Region } from './api';

	interface Props {
		regions: Region[];
	}

	let { regions }: Props = $props();
</script>

<!-- TODO add filter by name and filter by non-country (aka ISO2===null) -->
<div class=" grid w-full grid-flow-row grid-cols-5" aria-label="Regions">
	{#each regions as region}
		<a aria-label={region.iso3} href={`/regions/${region.iso3}${$page.url.search}`}>
			{region.name}
		</a>
	{/each}
</div>
