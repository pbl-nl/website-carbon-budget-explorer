<!-- { filename: './components/Scatter.svelte' } -->
<script lang="ts">
	// Import the getContext function from svelte
	import { getContext } from 'svelte';

	// Access the context using the 'LayerCake' keyword
	// Grab some helpful functions
	const { data, x, xScale, y, yScale } = getContext<any>('LayerCake');

	interface Props {
		fill?: string;
		r?: number;
	}

	let { fill = '#000', r = 5 }: Props = $props();
</script>

<g>
	{#each $data as d}
		<circle cx={$xScale($x(d))} cy={$yScale($y(d))} {fill} {r} />
	{/each}
</g>
