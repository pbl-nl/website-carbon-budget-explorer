<script lang="ts">
	import type { Region } from './api';

	let {
		regions,
		title
	}: {
		regions: Region[];
		title: string;
	} = $props();
</script>

<details class="dropdown drop">
	<summary class="btn btn-ghost btn-xs font-normal">{title} &#9660;</summary>
	<ul
		class="menu dropdown-content rounded-box z-50 max-h-[70vh] w-max overflow-y-auto bg-base-100 p-2 shadow-sm"
	>
		{#each regions as region}
			<li>
				<a href={`/regions/${region.iso3}`} class="block w-full whitespace-nowrap px-2 py-1">
					{region.name}
				</a>
			</li>
		{/each}
	</ul>
</details>
