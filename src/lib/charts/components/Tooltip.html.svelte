<!--
  @component
  Generates a hover tooltip. It creates a slot with an exposed variable via
  `let:detail` that contains information about the event. Use the slot to
  populate the body of the tooltip using the exposed variable `detail`.
 -->
<script lang="ts">
	import type { ComponentEvents } from 'svelte';
	import type { SvelteComponent } from 'svelte';

	interface Props {
		evt?: ComponentEvents<SvelteComponent>;
		offset?: any;
		children?: import('svelte').Snippet;
	}

	let { evt = {}, offset = -5, children }: Props = $props();
</script>

{#if evt.detail}
	<div
		class="layercake-tooltip"
		style="
      top:{evt.detail.e.layerY + offset}px;
      left:{evt.detail.e.layerX}px;
    "
	>
		{@render children?.()}
	</div>
{/if}

<style>
	.layercake-tooltip {
		position: absolute;
		width: 150px;
		border: 1px solid #ccc;
		font-size: 13px;
		background: rgba(255, 255, 255, 0.85);
		transform: translate(-50%, -100%);
		padding: 5px;
		z-index: 15;
	}
</style>
