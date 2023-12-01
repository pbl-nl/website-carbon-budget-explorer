<script lang="ts">
	import CustomRange from '$lib/CustomRange.svelte';
	import type { PathWayQuery } from '$lib/api';

	export let query: PathWayQuery;
	export let choices: Record<keyof PathWayQuery, string[]>;
	export let onChange: (name: string, value: string) => void;

	let defaults = {
		temperature: choices.temperature[Math.floor(choices.temperature.length / 2)],
		exceedanceRisk: choices.exceedanceRisk[Math.floor(choices.exceedanceRisk.length / 2)],
		negativeEmissions: choices.negativeEmissions[Math.floor(choices.negativeEmissions.length / 2)]
	};

	let temperature: string = query.temperature || defaults.temperature;
	let exceedanceRisk: string = query.exceedanceRisk || defaults.exceedanceRisk;
	let negativeEmissions: string = query.negativeEmissions || defaults.negativeEmissions;

	$: onChange('temperature', temperature);
	$: onChange('exceedanceRisk', exceedanceRisk);
	$: onChange('negativeEmissions', negativeEmissions);
</script>

<div class="card-compact card prose min-w-full bg-base-100 shadow-xl">
	<div class="card-body">
		<div>
			<h2 class="not-prose card-title">Global budget</h2>
			<p class="italic">How much do we have left?</p>
			<p>
				Limit global warming to (&deg;C)
				<span
					class="tooltip text-lg"
					data-tip="The temperature target determines the emissions we can globally still emit. A
			less ambitious target (for example, 2.2°C) implies the possibility to emit more greenhouse gases."
					>ⓘ</span
				>
				<CustomRange
					bind:value={temperature}
					options={choices.temperature.map((d) => Number(d))}
					name="temperature"
				/>
			</p>
			<p>
				Acceptable risk of exceeding global warming limit
				<span
					class="tooltip z-[750] text-lg"
					data-tip="The temperature rise at any level of cumulative emissions has some uncertainties.
					Therefore, if you want to be sure to remain within a given temperature level (small risk), you will need to shrink the budget even more."
					>ⓘ</span
				>
				<CustomRange
					bind:value={exceedanceRisk}
					options={choices.exceedanceRisk.map((d) => Number(d))}
					name="risk"
				/>
			</p>
			<h2 class="not-prose card-title">Global pathway</h2>
			<p><i>How do we spend these emissions over time?</i></p>
			<p>
				End-of-century negative emissions
				<span
					class="tooltip text-lg"
					data-tip="A major influence on the shape of the global pathway is the assumption on the amount of negative emissions.
					More negative emissions (slider to the right) gives us some slack in the coming decades, and vice versa."
					>ⓘ</span
				>
				<CustomRange
					bind:value={negativeEmissions}
					options={choices.negativeEmissions.map((d) => Number(d))}
					name="negEmis"
				/>
			</p>
		</div>
	</div>
</div>
