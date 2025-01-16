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
	interface Props {
		data: Row[];
		x?: string;
		y0?: string;
		y1?: string;
		color?: string;
	}

	let {
		data,
		x = 'x',
		y0 = 'y0',
		y1 = 'y1',
		color = '#ab00d6'
	}: Props = $props();

	let shade = $derived(area<Row>()
		.x((d) => $xScale(d[x]))
		.y1((d) => $yScale(d[y1]))
		.y0((d) => $yScale(d[y0]))
		.curve(curveLinear));
	let path = $derived(shade(data));

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
	onmouseover={hover}
	onmousemove={hover}
	onfocus={(e) => dispatch('mouseover', { e })}
	onmouseout={() => dispatch('mouseout')}
	onblur={() => dispatch('mouseout')}
	role="tooltip"
/>

<style>
	.path-area {
		fill-opacity: 0.2;
	}
</style>
