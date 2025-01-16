<script lang="ts">
	import { scaleOrdinal } from 'd3';
	import { LayerCake, Svg } from 'layercake';
	import type { PieData } from './components/Pie';
	import Pie from './components/Pie.svelte';

	interface Props {
		used: number;
		remaining: number;
	}

	let { used, remaining }: Props = $props();

	let data = $derived([
		['used', used],
		['remaining', remaining]
	] as PieData[]);

	const seriesColors = ['red', 'green'];
</script>

<div class="chart-container">
	<LayerCake z={0} zScale={scaleOrdinal()} zRange={seriesColors} {data}>
		<Svg>
			<Pie />
		</Svg>
	</LayerCake>
</div>

<style>
	/*
      The wrapper div needs to have an explicit width and height in CSS.
      It can also be a flexbox child or CSS grid element.
      The point being it needs dimensions since the <LayerCake> element will
      expand to fill it.
    */
	.chart-container {
		width: 500px;
		height: 500px;
	}
</style>
