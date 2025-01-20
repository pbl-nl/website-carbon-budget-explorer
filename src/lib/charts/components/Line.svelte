<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script lang="ts">
	import { bisector, type ScaleLinear } from 'd3';
	import { getContext } from 'svelte';
	import type { Readable } from 'svelte/store';

	const { xScale, yScale } = getContext<{
		xScale: Readable<ScaleLinear<number, number, never>>;
		yScale: Readable<ScaleLinear<number, number, never>>;
	}>('LayerCake');


	
	interface Props {
		data: Record<string, number>[];
		x?: string;
		y?: string;
		color?: string;
		mouseout?: (e?: any) => void;
		mouseover?: (e: any) => void;
	}

	let {
		data,
		x = 'x',
		y = 'y',
		color = '#ab00d6',
		mouseout = () => {},
		mouseover = () => {},
	}: Props = $props();

	let path =
		$derived('M' +
		data
			.filter(d => d[x] && d[y])
			.map((d) => {
				return $xScale(d[x]) + ',' + $yScale(d[y]);
			})
			.join('L'));

	const finder = bisector((d: (typeof data)[number]) => d[x]);
</script>

<path
	class="path-line"
	d={path}
	stroke={color}
	onmouseover={(e) => {
		const ox = $xScale.invert(e.offsetX);
		// find entry in data which is closest to ox
		const i = finder.center(data, ox);
		return mouseover({ e, row: data[i] });
	}}
	onmouseout={(e) => mouseout({ e })}
	onfocus={(e) => mouseover({ e })}
	onblur={() => mouseout()}
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
