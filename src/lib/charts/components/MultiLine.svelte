<!--
    @component
    Generates an SVG multi-series line chart with shading for uncertainty.

	Paths are animated using svelte transitions, see
	https://svelte.dev/docs/svelte-transition#draw

    Data should look like this:

    const data = [
		{
			stroke: ipcc_stroke_red,
			fill: ipcc_fill_red,
			values: [
				{ x: 2000, y: 61, y0: 60, y1: 64 },
				{ x: 2005, y: 56, y0: 51, y1: 58 },
				...
			]
		},
		{
			...
		}
	]
 -->
<script lang="ts">
	import { getContext } from 'svelte';
	import { area, line as d3line, curveLinear } from 'd3-shape';
	import { draw, fade } from 'svelte/transition';
	import { linear, sineIn } from 'svelte/easing';
	import type { Readable } from 'svelte/motion';
	import type { ScaleLinear } from 'd3';
	import type { LineData, LineValue } from './MultiLine';

	const { data, xGet, yGet, yScale } = getContext<{
		data: Readable<LineData[]>;
		xGet: Readable<number>;
		yGet: Readable<number>;
		yScale: Readable<ScaleLinear<number, number, never>>;
	}>('LayerCake');

	let curve = curveLinear;
	let line = $derived(d3line<LineValue>().x($xGet).y($yGet).curve(curve));
	let shade = $derived(area<LineValue>()
		.x($xGet)
		.y1((d) => $yScale(d.ymax))
		.y0((d) => $yScale(d.ymin))
		.curve(curve));
</script>

<g class="line-group">
	{#each $data as group}
		<path
			in:fade={{ duration: 2000, delay: 2000, easing: sineIn }}
			class="path-area"
			d={shade(group.values)}
			fill={group.fill}
		/>
		<path
			in:draw={{ duration: 2000, delay: 0, easing: linear }}
			class="path-line"
			d={line(group.values)}
			stroke={group.stroke}
		/>
	{/each}
</g>

<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 3px;
	}
	.path-area {
		fill-opacity: 0.8;
	}
</style>
