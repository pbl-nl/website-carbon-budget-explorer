<script lang="ts">
	import { run } from 'svelte/legacy';

	import { cubicOut } from 'svelte/easing';
	import { tweened } from 'svelte/motion';

	import { allocationMethods } from '$lib/allocationMethods';

	interface Props {
		reductions: Record<string, Record<number, number>>;
		activeAllocationMethods: Record<string, boolean>;
		availableAllocationMethods: Set<string>;
	}

	let {
		reductions,
		activeAllocationMethods = $bindable(),
		availableAllocationMethods
	}: Props = $props();
	const tweenOptions = { duration: 1000, easing: cubicOut };
	const tweenedReductions = tweened(reductions, tweenOptions);
	run(() => {
		tweenedReductions.set(reductions);
	});
	const grandfatheringColor = 'text-gray-400';
</script>

<div class="rounded px-12 py-8">
	<table class="prose w-full max-w-none table-auto">
		<thead>
			<tr>
				<th>Allocation method</th>
				{#each Object.values(allocationMethods) as { label }}
					<th>
						{#if label==='Grandfathering'}
							<span class={grandfatheringColor}>{label}</span>
						{:else}
							{label}
						{/if}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			<tr>
				<th>2030 reductions<br />relative to 2015</th>
				{#each Object.keys(allocationMethods) as id}
					<td class={id==='GF' ? grandfatheringColor : ""}>
							{reductions[id][2030] === null ? '-' : $tweenedReductions[id][2030].toFixed(0)}%
					</td>
				{/each}
			</tr>
			<tr>
				<th>2040 reductions<br />relative to 2015</th>
				{#each Object.keys(allocationMethods) as id}
					<th>
						<span class={id === 'GF' ? grandfatheringColor : ''}>
							{reductions[id][2040] === null ? '-' : $tweenedReductions[id][2040].toFixed(0)}%
						</span>
					</th>
				{/each}
			</tr>
			<tr>
				<th>Display graph</th>
				{#each Object.entries(allocationMethods) as [id, { color }]}
					<th>
						{#if availableAllocationMethods.has(id)}
							<input
								type="checkbox"
								bind:checked={activeAllocationMethods[id]}
								style={`background-color: ${color}`}
								class="m-1 scale-125 shadow"
								disabled={!availableAllocationMethods.has(id)}
							/>
						{:else}
							<input
								type="checkbox"
								disabled
								class="m-1 scale-125 bg-gray-200 shadow"
								title="Not available for this region"
							/>
						{/if}
					</th>
				{/each}
			</tr>
		</tbody>
	</table>
</div>
