<!--
  @component
  Generates an SVG x-axis. This component is also configured to detect if your x-scale is an ordinal scale. If so, it will place the markers in the middle of the bandwidth.
 -->
<script>
	import { getContext } from 'svelte';
	const { width, height, xScale, yRange } = getContext('LayerCake');

	

	

	

	

	/** @type {Function} [formatTick=d: any => d] - A function that passes the current tick value and expects a nicely formatted value in return. */
	

	

	

	
	/**
	 * @typedef {Object} Props
	 * @property {Boolean} [gridlines]
	 * @property {Boolean} [tickMarks]
	 * @property {Boolean} [baseline]
	 * @property {Boolean} [snapTicks]
	 * @property {any} [formatTick]
	 * @property {Number|Array<any>|Function|undefined} [ticks]
	 * @property {Number} [xTick]
	 * @property {Number} [yTick]
	 */

	/** @type {Props} */
	let {
		gridlines = true,
		tickMarks = false,
		baseline = false,
		snapTicks = false,
		formatTick = (d) => d,
		ticks = undefined,
		xTick = 0,
		yTick = 16
	} = $props();

	let isBandwidth = $derived(typeof $xScale.bandwidth === 'function');

	let tickVals = $derived(Array.isArray(ticks)
		? ticks
		: isBandwidth
		? $xScale.domain()
		: typeof ticks === 'function'
		? ticks($xScale.ticks())
		: $xScale.ticks(ticks));

	// @ts-expect-error: copied from https://layercake.graphics/components
	function textAnchor(i) {
		if (snapTicks === true) {
			if (i === 0) {
				return 'start';
			}
			if (i === tickVals.length - 1) {
				return 'end';
			}
		}
		return 'middle';
	}
</script>

<g class="axis x-axis" class:snapTicks>
	{#each tickVals as tick, i (tick)}
		<g class="tick tick-{i}" transform="translate({$xScale(tick)},{Math.max(...$yRange)})">
			{#if gridlines !== false}
				<line class="gridline" y1={$height * -1} y2="0" x1="0" x2="0" />
			{/if}
			{#if tickMarks === true}
				<line
					class="tick-mark"
					y1={0}
					y2={6}
					x1={isBandwidth ? $xScale.bandwidth() / 2 : 0}
					x2={isBandwidth ? $xScale.bandwidth() / 2 : 0}
				/>
			{/if}
			<text
				x={isBandwidth ? $xScale.bandwidth() / 2 + xTick : xTick}
				y={yTick}
				dx=""
				dy=""
				text-anchor={textAnchor(i)}>{formatTick(tick)}</text
			>
		</g>
	{/each}
	{#if baseline === true}
		<line class="baseline" y1={$height + 0.5} y2={$height + 0.5} x1="0" x2={$width} />
	{/if}
</g>

<style>
	.tick {
		font-size: 1rem;
		font-weight: 200;
	}

	line,
	.tick line {
		stroke: #aaa;
		stroke-dasharray: 2;
	}

	.tick text {
		fill: #666;
	}

	.tick .tick-mark,
	.baseline {
		stroke-dasharray: 0;
	}
	/* This looks slightly better */
	.axis.snapTicks .tick:last-child text {
		transform: translateX(3px);
	}
	.axis.snapTicks .tick.tick-0 text {
		transform: translateX(-3px);
	}
</style>
