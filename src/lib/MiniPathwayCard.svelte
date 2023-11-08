<script lang="ts">
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	import { page } from '$app/stores';
	import Pathway from '$lib/charts/Pathway.svelte';
	import Line from '$lib/charts/components/Line.svelte';
	import Area from '$lib/charts/components/Area.svelte';
	import type { CertainTime, UncertainTime } from '$lib/api';

	export let global: {
		pathwayCarbon: UncertainTime[];
		historicalCarbon: CertainTime[];
		currentPolicy: UncertainTime[];
	};

	const ipcc_green = '#82a56e';
	const ipcc_red = '#f5331e';

	const tweenOptions = { duration: 1000, easing: cubicOut };
	const pathwayCarbonTweened = tweened(global.pathwayCarbon, tweenOptions);
	$: pathwayCarbonTweened.set(global.pathwayCarbon);

	// TODO add tooltips for each area
</script>

<div class="card-compact card flex-1 bg-base-100 shadow-xl">
	<div class="card-body">
		<a class="block h-full w-full" href={`/global${$page.url.search}`}>
			<!-- TODO on x-axis have less or no ticks, now they are overlapping and unreadable -->
			<!-- TODO would be cool when you navigate from /global to /map this chart would view transition from full screen to minimap -->
			<!-- TODO would be nice when you hover over line or area it would show tooltip with series description -->
			<Pathway xTicks={3} yTicks={4}>
				<Line data={global.historicalCarbon} x={'time'} y={'value'} color="black" />
				<Line data={$pathwayCarbonTweened} x={'time'} y={'mean'} color={ipcc_green} />
				<Area data={$pathwayCarbonTweened} x={'time'} y0={'min'} y1={'max'} color={ipcc_green} />
				<Line data={global.currentPolicy} x={'time'} y={'mean'} color={ipcc_red} />
				<Area data={global.currentPolicy} x={'time'} y0={'min'} y1={'max'} color={ipcc_red} />
			</Pathway>
		</a>
	</div>
</div>
