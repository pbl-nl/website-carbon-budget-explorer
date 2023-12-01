<script lang="ts">
	// See https://observablehq.com/@d3/color-legend
	// and https://observablehq.com/@slowkow/vertical-color-legend
	import type { ScaleSequential } from 'd3-scale';
	import { format, interpolateRound, quantile, range } from 'd3';

	export let title: string;
	export let scale: ScaleSequential<string, never>;

	function ramp(color: any, n = 256) {
		const canvas = document.createElement('canvas');
		canvas.height = n;
		canvas.width = 1;
		const context = canvas.getContext('2d');
		for (let i = 0; i < n; ++i) {
			context!.fillStyle = color(i / (n - 1));
			context!.fillRect(0, n - i, 1, 1);
		}
		return canvas;
	}

	const tickSize = 6;
	const width = 36 + tickSize;
	const height = 320;
	const marginTop = 20;
	const marginRight = 10 + tickSize;
	const marginBottom = 20;
	const marginLeft = 5;
	const ticks = height / 64;

	$: y = Object.assign(
		scale.copy().interpolator(interpolateRound(marginBottom, height - marginTop)),
		{
			range() {
				return [marginBottom, height - marginTop];
			}
		}
	);
	$: tickValues = range(ticks + 1).map((i) => quantile(scale.domain(), i / ticks));
	const tickFormat = format('.4');
</script>

<div class="absolute bottom-40 right-14 z-[400]">
	<svg {width} {height} viewBox={`0 0 ${width} ${height}`} overflow="visible" display="block">
		>
		<image
			width={width - marginRight - marginLeft}
			height={height - marginTop - marginBottom}
			x={marginLeft}
			y={marginTop}
			preserveAspectRatio="none"
			xlink:href={ramp(scale.interpolator()).toDataURL()}
		/>
		<g transform={`translate(26,0)`}>
			{#each tickValues as tick (tick)}
				<g class="tick" transform={`translate(0, ${height - y(tick || 0) + 0.5})`}>
					<text fill="currentColor" x={tickSize + 3} dy=".32em">
						{tickFormat(tick || 0)}
					</text>
				</g>
			{/each}
			<text
				fill="currentColor"
				x={-50}
				y={0}
				transform="translate(-35, 250) rotate(270)"
				text-anchor="start"
				font-weight="bold"
				font-size="14px">{title}</text
			>
		</g>
	</svg>
</div>
