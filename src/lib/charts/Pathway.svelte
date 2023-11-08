<script lang="ts">
	import { Html, LayerCake, Svg } from 'layercake';
	import AxisX from './components/AxisX.svelte';
	import AxisY from './components/AxisY.svelte';
	import Tooltip from './components/Tooltip.html.svelte';
	import type { ComponentEvents, SvelteComponent } from 'svelte';

	export let xDomain: [number, number] = [1990, 2100];
	export let yDomain: [number, number] = [0, 60];
	export let evt: ComponentEvents<SvelteComponent> = {};
	export let yAxisTtle = '';
	export let xTicks: number | Array<any> | undefined = undefined;
	export let yTicks: number | Array<any> | undefined = 8;
</script>

<div class="h-full w-full overflow-clip pb-5 pl-12 pr-5 pt-1">
	<LayerCake {xDomain} {yDomain}>
		<Svg>
			<AxisX gridlines={true} ticks={xTicks} />
			<AxisY gridlines={true} ticks={yTicks} textAnchor={'end'} title={yAxisTtle} />
			<slot />
		</Svg>
		<Html pointerEvents={false}>
			{#if evt?.detail?.msg}
				<Tooltip {evt}>
					{evt.detail.msg}
				</Tooltip>
			{/if}
		</Html>
	</LayerCake>
</div>
