<script lang="ts">
	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

<div id="sidebar" class="flex h-full w-1/3 flex-col place-content-stretch gap-4 2xl:w-1/4">
	{@render children?.()}
</div>
