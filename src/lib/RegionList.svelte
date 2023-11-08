<script lang="ts">
	import { page } from '$app/stores';
	import type { Region } from './api';

	export let regions: Region[];
</script>

<!-- TODO add filter by name and filter by non-country (aka ISO2===null) -->
<div class=" grid w-full grid-flow-row grid-cols-5">
	{#each regions as region}
		<a href={`/regions/${region.iso3}${$page.url.search}`}>
			{region.name}
		</a>
	{/each}
</div>
