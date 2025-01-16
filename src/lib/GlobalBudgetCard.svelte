<script lang="ts">
	import { run } from 'svelte/legacy';

	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	interface Props {
		remaining: number;
		relative: number;
	}

	let { remaining, relative }: Props = $props();

	const tweenOptions = { duration: 1000, easing: cubicOut };
	const remainingBudgetCounter = tweened(remaining, tweenOptions);
	run(() => {
		remainingBudgetCounter.set(remaining);
	});
	const relativeBudgetCounter = tweened(relative, tweenOptions);
	run(() => {
		relativeBudgetCounter.set(relative);
	});
</script>

<div class="grid min-w-full grid-cols-2 place-items-center rounded bg-base-100 p-2 shadow-xl">
	<div class="text-center text-base-content/60">Global carbon budget</div>
	<div class="text-center text-base-content/60">That amounts to</div>

	<div class="text-4xl font-extrabold">{$remainingBudgetCounter.toFixed()}</div>
	<div class="text-4xl font-extrabold">
		{$relativeBudgetCounter.toFixed()}x
	</div>

	<div class="text-center text-xs text-base-content/60" title="Gigaton carbon dioxide">Gt CO₂</div>
	<div class="text-center text-xs text-base-content/60">the current annual emissions</div>
</div>
