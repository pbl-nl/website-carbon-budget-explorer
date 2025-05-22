<script lang="ts">
	import clsx from 'clsx';

	interface Props {
		className?: string;
		children?: import('svelte').Snippet;
	}

	let { children, className}: Props = $props();
</script>

<div id="sidebar" class={clsx("flex h-full w-1/3 flex-col place-content-stretch gap-4 2xl:w-1/4", className)}>
	{@render children?.()}
</div>
