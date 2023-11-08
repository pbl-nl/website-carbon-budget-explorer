<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script lang="ts">
	import { bisector, type ScaleLinear } from 'd3';
	import { area, curveLinear } from 'd3-shape';
	import { createEventDispatcher, getContext, SvelteComponent, type ComponentEvents } from 'svelte';
	import type { Readable } from 'svelte/store';

	const { xScale, yScale } = getContext<{
		xScale: Readable<ScaleLinear<number, number, never>>;
		yScale: Readable<ScaleLinear<number, number, never>>;
	}>('LayerCake');

	type Row = Record<string, number>;
	export let data: Row[];
	export let x = 'x';
	export let y0 = 'y0';
	export let y1 = 'y1';
	export let color = '#ab00d6';

	$: shade = area<Row>()
		.x((d) => $xScale(d[x]))
		.y1((d) => $yScale(d[y1]))
		.y0((d) => $yScale(d[y0]))
		.curve(curveLinear);
	$: path = shade(data);

	const dispatch = createEventDispatcher();
	const finder = bisector((d: (typeof data)[number]) => d[x]);

	function hover(e: ComponentEvents<SvelteComponent>) {
		const ox = $xScale.invert(e.offsetX);
		// find entry in data which is closest to ox
		const i = finder.center(data, ox);
		return dispatch('mouseover', { e, row: data[i] });
	}
</script>

<path
	class="path-area"
	d={path}
	fill={color}
	on:mouseover={hover}
	on:mousemove={hover}
	on:focus={(e) => dispatch('mouseover', { e })}
	on:mouseout={() => dispatch('mouseout')}
	on:blur={() => dispatch('mouseout')}
	role="tooltip"
/>

<style>
	.path-area {
		fill-opacity: 0.2;
	}
</style>
