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

	export let x: number;
	export let y0: number;
	export let y1: number;
	export let width = 20;

	export let color = '#888888';
</script>

<g>
	<rect
		x={$xScale(x) - width / 2}
		y={$yScale(y0)}
		{width}
		height={$yScale(y1) - $yScale(y0)}
		fill={color}
		opacity="0.25"
	/>
	<line
		x1={$xScale(x)}
		x2={$xScale(x)}
		y1={$yScale(y1)}
		y2={$yScale(y0)}
		stroke={color}
		stroke-dasharray="4"
	/>
	<line
		x1={$xScale(x) - width / 2}
		x2={$xScale(x) + width / 2}
		y1={$yScale(y0)}
		y2={$yScale(y0)}
		stroke={color}
	/>
	<line
		x1={$xScale(x) - width / 2}
		x2={$xScale(x) + width / 2}
		y1={$yScale(y1)}
		y2={$yScale(y1)}
		stroke={color}
	/>
	<text x={$xScale(x) + width} y={($yScale(y0) + $yScale(y1)) / 2}
		>{Math.abs(y1 - y0).toFixed()} Gt CO₂e</text
	>
	<!-- <line x1=x, x2=x, y1=y0, y2=y1></line>
	<line x1=x, x2=x, y1=y0, y2=y1></line> -->
</g>

<style>
	line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 2;
	}
</style>
