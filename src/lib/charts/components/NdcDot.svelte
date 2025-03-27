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
		y: number;
		width?: number;
		textNdc: string;
		text4Dot: string;
		// TODO use color of ndc series on global page?
		color?: string;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		mouseover: (e?: any) => void;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		mouseout: (e?: any) => void;
	}

	let {
		x,
		y,
		width = 2,
		textNdc,
		text4Dot,
		color = 'black',
		mouseover,
		mouseout
	}: Props = $props();

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function hover(e: any) {
		return mouseover({ e, row: { time: x, min: y, max: y } });
	}
</script>

<g id="ndc">
	<text
		x={$xScale(x)}
		y={$yScale(y) - 18}
		fill={color}
		text-anchor="middle"
		font-size="15px"
		class="text-container"
	>
		{text4Dot}
	</text>
	<text
		x={$xScale(x) - 60}
		y={$yScale(y) + 8}
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
		cy={$yScale(y)}
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
	.text-container {
		position: relative; /* or absolute/fixed if needed */
		z-index: 9999; /* High value to ensure it is on top */
		background: white; /* Optional: to ensure text is readable */
	}
</style>
