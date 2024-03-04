<script lang="ts">
	import CustomRange from '$lib/CustomRange.svelte';
	import type { PathWayQuery } from '$lib/api';

	export let query: PathWayQuery;
	export let choices: Record<keyof PathWayQuery, string[]>;
	export let onChange: (name: string, value: string) => void;

	let defaults = {
		temperature: '2.0',
		exceedanceRisk: '0.5',
		negativeEmissions: '0.5',
		timing: 'Immediate',
		nonCO2red: '0.5'
	};

	let temperature: string = query.temperature || defaults.temperature;
	let exceedanceRisk: string = query.exceedanceRisk || defaults.exceedanceRisk;
	let negativeEmissions: string = query.negativeEmissions || defaults.negativeEmissions;
	let timing: string = query.timing || defaults.timing;
	let nonCO2red: string = query.nonCO2red || defaults.nonCO2red;

	$: onChange('temperature', temperature);
	$: onChange('exceedanceRisk', exceedanceRisk);
	$: onChange('negativeEmissions', negativeEmissions);
	$: onChange('timing', timing);
	$: onChange('nonCO2red', nonCO2red);
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
					data-tip="The peak temperature target determines the emissions we can globally still emit. A
			less ambitious target (for example, 2.2°C) implies the possibility to emit more greenhouse gases."
					>ⓘ</span
				>
				<CustomRange
					bind:value={temperature}
					options={choices.temperature.map((d) => String(d))}
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
					options={choices.exceedanceRisk.map((d) => String(d))}
					name="risk"
				/>
			</p>
			<p>
				Reduction of non-CO<sub>2</sub> emissions
				<span
					class="tooltip z-[750] text-lg"
					data-tip="Not only CO2, but also other gases play a role in the global emissions trajectory. Setting this slider to low values assumes small reductions in non-CO2 by 2040, which means that CO2 has to reduce much more, and vica versa.
							  In the graph to the right, we show all greenhouse gases (CO2 and non-CO2), so the green line will barely move if you adjust this slider, as the temperature goal remains fixed.
							  However, this does greatly affect the carbon budget (which is only the CO2 part) in the top-left corner of your screen."
					>ⓘ</span
				>
				<CustomRange
					bind:value={nonCO2red}
					options={choices.nonCO2red.map((d) => String(d))}
					name="nonCO2red"
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
					options={choices.negativeEmissions.map((d) => String(d))}
					name="negEmis"
				/>
			</p>
			<p>
				The timing of early-century mitigation
				<span
					class="tooltip text-lg"
					data-tip="Analogous to IPCC WGIII scenarios, we distinguish global emission pathways with delayed (i.e., near-similar emissions up to 2030) and immediate action. Delayed action is infeasible with a temperature target of 1.5, so identical data will be shown in that case."
					>ⓘ</span
				>
				<CustomRange
					bind:value={timing}
					options={choices.timing.map((d) => String(d))}
					name="timing"
				/>
			</p>
		</div>
	</div>
</div>
