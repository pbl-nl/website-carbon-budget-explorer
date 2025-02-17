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
		x: number;
		y0: number;
		y1: number;
		width?: number;
		textNdcMin: string;
		textNdcMax: string;
		textNdc: string;
		// TODO use color of ndc series on global page?
		color?: string;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		mouseover: (e?: any) => void;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		mouseout: (e?: any) => void;
	}

	let {
		x,
		y0,
		y1,
		width = 2,
		textNdcMin,
		textNdcMax,
		textNdc,
		color = 'black',
		mouseover,
		mouseout
	}: Props = $props();

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function hover(e: any) {
		return mouseover({ e, row: { time: x, min: y0, max: y1 } });
	}
</script>

<g id="ndc">
	<line
		x1={$xScale(x)}
		x2={$xScale(x)}
		y1={$yScale(y1)}
		y2={$yScale(y0)}
		stroke={color}
		onmouseover={hover}
		onfocus={() => mouseover()}
		onmouseout={() => mouseout()}
		onblur={() => mouseout()}
		role="tooltip"
	/>
	<circle
		cx={$xScale(x)}
		r={width * 2}
		cy={$yScale(y0)}
		stroke={color}
		fill={color}
		onmouseover={hover}
		onfocus={() => mouseover()}
		onmouseout={() => mouseout()}
		onblur={() => mouseout()}
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
		onmouseover={hover}
		onfocus={() => mouseover()}
		onmouseout={() => mouseout()}
		onblur={() => mouseout()}
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
