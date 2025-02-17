<script lang="ts">
	import { Html, LayerCake, Svg } from 'layercake';
	import AxisX from './components/AxisX.svelte';
	import AxisY from './components/AxisY.svelte';
	import Tooltip from './components/Tooltip.html.svelte';
	import type { ComponentEvents, SvelteComponent } from 'svelte';

	interface Props {
		xDomain?: [number, number];
		yDomain?: [number, number];
		evt?: ComponentEvents<SvelteComponent>;
		yAxisTtle?: string;
		xTicks?: number | Array<number> | undefined;
		yTicks?: number | Array<number> | undefined;
		children?: import('svelte').Snippet;
	}

	let {
		xDomain = [1990, 2100],
		yDomain = [-10, 70],
		evt = {},
		yAxisTtle = '',
		xTicks = undefined,
		yTicks = 8,
		children
	}: Props = $props();
</script>

<div class="h-full w-full overflow-clip pb-5 pl-12 pr-5 pt-1">
	<LayerCake {xDomain} {yDomain}>
		<Svg>
			<AxisX gridlines={true} ticks={xTicks} />
			<AxisY gridlines={true} ticks={yTicks} textAnchor={'end'} title={yAxisTtle} />
			{@render children?.()}
		</Svg>
		<Html pointerEvents={false}>
			{#if evt?.msg}
				<Tooltip {evt}>
					{evt.msg}
				</Tooltip>
			{/if}
		</Html>
	</LayerCake>
</div>
