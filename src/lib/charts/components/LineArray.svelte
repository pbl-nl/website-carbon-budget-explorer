<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script lang="ts">
	import type { ScaleLinear } from 'd3';
	import { getContext } from 'svelte';
	import type { Readable } from 'svelte/store';

	const { xScale, yScale } = getContext<{
		xScale: Readable<ScaleLinear<number, number, never>>;
		yScale: Readable<ScaleLinear<number, number, never>>;
	}>('LayerCake');


	
	interface Props {
		data: Record<string, number[]>;
		x?: string;
		y?: string;
		color?: string;
	}

	let {
		data,
		x = 'x',
		y = 'y',
		color = '#ab00d6'
	}: Props = $props();

	let path =
		$derived('M' +
		data[x]
			.map((d, i) => {
				return $xScale(d) + ',' + $yScale(data[y][i]);
			})
			.join('L'));
</script>

<path class="path-line" d={path} stroke={color} />

<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 2;
	}
</style>
