<script lang="ts">
	import clsx from 'clsx';

	let active = $state(false);
	interface Props {
		question?: string;
		children?: import('svelte').Snippet;
	}

	let { question = 'question', children }: Props = $props();
</script>

<div class="transition-all">
	<label class="cursor-pointer transition-all">
		<input type="checkbox" bind:checked={active} class="hidden" />
		<h3>
			<span class={clsx(active && 'inline-flex rotate-90', 'transition-all')}>⮚</span>
			{question}
		</h3></label
	>
	<div class={clsx('prose px-2', !active && 'hidden')}>
		{#if children}{@render children()}{:else}<p>Answer</p>{/if}
	</div>
</div>
