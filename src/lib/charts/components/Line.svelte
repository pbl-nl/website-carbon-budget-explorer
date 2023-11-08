<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script lang="ts">
	import { bisector, type ScaleLinear } from 'd3';
	import { createEventDispatcher, getContext } from 'svelte';
	import type { Readable } from 'svelte/store';

	const { xScale, yScale } = getContext<{
		xScale: Readable<ScaleLinear<number, number, never>>;
		yScale: Readable<ScaleLinear<number, number, never>>;
	}>('LayerCake');

	export let data: Record<string, number>[];
	export let x = 'x';
	export let y = 'y';

	/** @type {String} [stroke='#ab00d6'] - The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
	export let color = '#ab00d6';

	$: path =
		'M' +
		data
			.map((d) => {
				return $xScale(d[x]) + ',' + $yScale(d[y]);
			})
			.join('L');

	const dispatch = createEventDispatcher();
	const finder = bisector((d: (typeof data)[number]) => d[x]);
</script>

<path
	class="path-line"
	d={path}
	stroke={color}
	on:mouseover={(e) => {
		const ox = $xScale.invert(e.offsetX);
		// find entry in data which is closest to ox
		const i = finder.center(data, ox);
		return dispatch('mouseover', { e, row: data[i] });
	}}
	on:mouseout={(e) => dispatch('mouseout', { e })}
	on:focus={(e) => dispatch('mouseover', { e })}
	on:blur={() => dispatch('mouseout')}
	role="tooltip"
/>

<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 4;
	}
</style>
