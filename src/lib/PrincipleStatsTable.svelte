<script lang="ts">
	import { run } from 'svelte/legacy';

	import { cubicOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';

	import { principles } from '$lib/principles';

	interface Props {
		reductions: Record<string, Record<number, number>>;
		activeEffortSharings: Record<string, boolean>;
	}

	let { reductions, activeEffortSharings = $bindable() }: Props = $props();
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedReductions = tweened(reductions, tweenOptions);
	run(() => {
		tweenedReductions.set(reductions);
	});
</script>

<div class="rounded px-12 py-8">
	<table class="prose w-full max-w-none table-auto">
		<thead>
			<tr>
				<th>Allocation method</th>
				{#each Object.values(principles) as { label }}
					<th>{label}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			<tr>
				<th>2030 reductions<br />relative to 2015</th>
				{#each Object.keys(principles) as id}
					<th>{reductions[id][2030] === null ? '-' : $tweenedReductions[id][2030].toFixed(0)}%</th>
				{/each}
			</tr>
			<tr>
				<th>2040 reductions<br />relative to 2015</th>
				{#each Object.keys(principles) as id}
					<th>{reductions[id][2040] === null ? '-' : $tweenedReductions[id][2040].toFixed(0)}%</th>
				{/each}
			</tr>
			<tr>
				<th>Display graph</th>
				{#each Object.entries(principles) as [id, { color }]}
					<th
						><input
							type="checkbox"
							bind:checked={activeEffortSharings[id]}
							style={`background-color: ${color}`}
							class="m-1 scale-125 shadow"
						/></th
					>
				{/each}
			</tr>
		</tbody>
	</table>
</div>
