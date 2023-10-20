<script lang="ts">
	import CustomRange from './CustomRange.svelte';
	import type { PathWayQuery } from './api';

	export let query: PathWayQuery;
	export let choices: Record<keyof PathWayQuery, string[]>;
	export let onChange: (name: string, value: string) => void;

	let temperature: string = query.temperature || choices.temperature[0];
	let negEmis: string = query.negativeEmissions || choices.negativeEmissions[0];
	let nonCO2: string = query.nonCO2Mitigation || choices.nonCO2Mitigation[0];
	let risk: string = query.exceedanceRisk || choices.exceedanceRisk[0];
	$: onChange('temperature', temperature);
	$: onChange('negativeEmissions', negEmis);
	$: onChange('nonCO2Mitigation', nonCO2);
	$: onChange('exceedanceRisk', risk);
</script>

<div>
	<div>
		<p>Limit global warming to</p>
		<CustomRange
			bind:value={temperature}
			options={choices.temperature.map((d) => Number(d))}
			name="temperature"
		/>
	</div>
	<div>
		<p>Acceptable risk of exceeding global warming limit</p>
		<CustomRange
			bind:value={risk}
			options={choices.exceedanceRisk.map((d) => Number(d))}
			name="risk"
		/>
	</div>
	<div>
		<p>Assumption of non CO2 emissions to mitigate</p>
		<CustomRange
			bind:value={nonCO2}
			options={choices.nonCO2Mitigation.map((d) => Number(d))}
			name="nonCO2"
		/>
	</div>
	<div>
		<p>Assumption amount of negative emissions in 2050 - 2100.</p>
		<CustomRange
			bind:value={negEmis}
			options={choices.negativeEmissions.map((d) => Number(d))}
			name="negEmis"
		/>
	</div>
</div>
