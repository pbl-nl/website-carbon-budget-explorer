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

<div class="card card-compact prose bg-base-100 shadow-xl">
	<div class="card-body">
		<div>
			<h2 class="not-prose card-title">Global budget</h2>
			<p>How much to reduce?</p>
			<p>
				Limit global warming to (&deg;C)
				<span
					class="tooltip text-lg"
					data-tip="The temperature target determines how many greenhouse gases we can still emit, globally. A
			less ambitious target (for example, 2.2°C) means tolerating more emissions.">🛈</span
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
					class="tooltip text-lg"
					data-tip="The risk of exceeding the temperature target is also relevant to the budget. Less risk
						means that your budget is more to the 'safe' side.">🛈</span
				>
				<CustomRange
					bind:value={exceedanceRisk}
					options={choices.exceedanceRisk.map((d) => Number(d))}
					name="risk"
				/>
			</p>
			<h2 class="not-prose card-title">Global pathway</h2>
			<p>How quickly to reduce?</p>
			<p>
				Assumption on negative emissions in 2050 - 2100
				<span
					class="tooltip text-lg"
					data-tip="How quickly we need to reduce depends on the amount of negative emissions we expect to
					achieve in the future. With less negative emissions you need to reduce faster. The global
				budget remains the same.">🛈</span
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
