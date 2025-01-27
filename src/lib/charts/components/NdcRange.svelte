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
	export let textNdcMin: string;
	export let textNdcMax: string;
	export let textNdc: string;

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
		r={width * 2}
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
	<text
		x={$xScale(x)}
		y={$yScale(y0) + 30}
		fill={color}
		text-anchor="middle"
		font-size="15px"
		class="text-container"
	>
		{textNdcMin}
	</text>
	<text
		x={$xScale(x)}
		y={$yScale(y1) - 18}
		fill={color}
		text-anchor="middle"
		font-size="15px"
		class="text-container"
	>
		{textNdcMax}
	</text>
	<text
		x={$xScale(x) - 60}
		y={$yScale(y1) + 8}
		fill={color}
		text-anchor="middle"
		font-size="18px"
		font-weight="bold"
		class="text-container"
	>
		{textNdc}
	</text>
	<circle
		cx={$xScale(x)}
		r={width * 2}
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

	.text-container {
		position: relative; /* or absolute/fixed if needed */
		z-index: 9999; /* High value to ensure it is on top */
		background: white; /* Optional: to ensure text is readable */
	}
</style>
