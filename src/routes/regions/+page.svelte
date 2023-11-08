<script lang="ts">
	import RegionList from '$lib/RegionList.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<h1 class="text-3xl font-bold">Pick a region</h1>
<!-- TODO add world map to pick a country with -->
<div class="card-compact card bg-base-100 p-4 shadow-xl">
	<RegionList regions={data.regions} />
</div>
