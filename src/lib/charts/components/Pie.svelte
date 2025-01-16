<script lang="ts">
	import { run } from 'svelte/legacy';

	import type { PieArcDatum, ScaleOrdinal } from 'd3';
	import { arc as d3arc } from 'd3-shape';
	import { pie as d3pie } from 'd3-shape';
	import { getContext } from 'svelte';
	import { cubicInOut } from 'svelte/easing';
	import type { Readable } from 'svelte/store';
	import { tweened, type TweenedOptions } from 'svelte/motion';
	import type { PieData } from './Pie';

	const tweenOptions: TweenedOptions<PieData[]> = {
		duration: 1500,
		easing: cubicInOut
	};

	const { data, zScale, width, height } = getContext<{
		data: Readable<PieData[]>;
		zScale: Readable<ScaleOrdinal<string, string, never>>;
		width: Readable<number>;
		height: Readable<number>;
	}>('LayerCake');

	let radius = $derived(Math.min($width, $height) / 2 - 1);

	// Compute the position of each group on the pie:
	const pie = d3pie<unknown, PieData>()
		.sort(null) // Don't sort
		.sortValues(null) // Really don't sort
		.value((d) => d[1]);

	const animatedData = tweened<PieData[]>($data, tweenOptions);
	run(() => {
		animatedData.set($data);
	});

	let slices = $derived(pie($animatedData));
	let arcGenerator = $derived(d3arc<unknown, PieArcDatum<PieData>>().innerRadius(0).outerRadius(radius));
</script>

<g transform="translate({$width / 2}, {$height / 2})">
	{#each slices as slice}
		<path d={arcGenerator(slice)} fill={$zScale(slice.data[0])} stroke="black" />
		<text transform="translate({arcGenerator.centroid(slice)})">
			{slice.data[0]}
		</text>
	{/each}
</g>

<style>
	path {
		stroke-width: style2px;
		opacity: 0.7;
	}
	text {
		text-anchor: middle;
		font-size: 1.5em;
	}
</style>
