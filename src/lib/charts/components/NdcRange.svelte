<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script lang="ts">
	import type { ScaleLinear } from 'd3';
	import { getContext, SvelteComponent, type ComponentEvents, createEventDispatcher } from 'svelte';
	import type { Readable } from 'svelte/store';

	const { xScale, yScale } = getContext<{
		xScale: Readable<ScaleLinear<number, number, never>>;
		yScale: Readable<ScaleLinear<number, number, never>>;
	}>('LayerCake');

	export let x: number;
	export let y0: number;
	export let y1: number;
	export let width = 2;

	// TODO use color of ndc series on global page?
	export let color = 'black';
	const dispatch = createEventDispatcher();

	function hover(e: ComponentEvents<SvelteComponent>) {
		return dispatch('mouseover', { e, row: { time: x, min: y0, max: y1 } });
	}
</script>

<g id="ndc">
	<line
		x1={$xScale(x)}
		x2={$xScale(x)}
		y1={$yScale(y1)}
		y2={$yScale(y0)}
		stroke={color}
		on:mouseover={hover}
		on:focus={() => dispatch('mouseover')}
		on:mouseout={() => dispatch('mouseout')}
		on:blur={() => dispatch('mouseout')}
		on:mouseout={() => dispatch('mouseout')}
		role="tooltip"
	/>
	<circle
		cx={$xScale(x)}
		r={width}
		cy={$yScale(y0)}
		stroke={color}
		fill={color}
		on:mouseover={hover}
		on:focus={() => dispatch('mouseover')}
		on:mouseout={() => dispatch('mouseout')}
		on:blur={(e) => dispatch('mouseout')}
		on:mouseout={() => dispatch('mouseout')}
		role="tooltip"
	/>
	<circle
		cx={$xScale(x)}
		r={width}
		cy={$yScale(y1)}
		stroke={color}
		fill={color}
		on:mouseover={hover}
		on:focus={() => dispatch('mouseover')}
		on:mouseout={() => dispatch('mouseout')}
		on:blur={() => dispatch('mouseout')}
		on:mouseout={() => dispatch('mouseout')}
		role="tooltip"
	/>
</g>

<style>
	line {
		fill: none;
		stroke-width: 2;
	}
</style>
