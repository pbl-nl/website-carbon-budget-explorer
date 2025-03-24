<script lang="ts">
	import CustomRange from '$lib/CustomRange.svelte';
	import type { PathWayQuery } from '$lib/api';
	import CategoryPicker from './CategoryPicker.svelte';

	interface Props {
		query: PathWayQuery;
		options: Record<keyof PathWayQuery, string[]>;
		onChange: (name: string, value: string) => void;
	}

	let { query, options, onChange }: Props = $props();

	let temperature: string = $state(query.temperature);
	let exceedanceRisk: string = $state(query.exceedanceRisk);
	let negativeEmissions: string = $state(query.negativeEmissions);
	let timing: string = $state(query.timing);
	let nonCO2red: string = $state(query.nonCO2red);

	$effect(() => {
		if (query.temperature === temperature) {
			return;
		}
		onChange('temperature', temperature);
	});
	$effect(() => {
		if (query.exceedanceRisk === exceedanceRisk) {
			return;
		}
		onChange('exceedanceRisk', exceedanceRisk);
	});
	$effect(() => {
		if (query.negativeEmissions === negativeEmissions) {
			return;
		}
		onChange('negativeEmissions', negativeEmissions);
	});
	$effect(() => {
		if (query.timing === timing) {
			return;
		}
		onChange('timing', timing);
	});
	$effect(() => {
		if (query.nonCO2red === nonCO2red) {
			return;
		}
		onChange('nonCO2red', nonCO2red);
	});
</script>

<div class="card prose card-compact min-w-full bg-base-100 shadow-xl">
	<div class="card-body">
		<div>
			<h2 class="not-prose card-title">Global settings</h2>
			<p class="italic">How many emissions we have left is determined by:</p>
			<div class="block">
				Limit global warming to (&deg;C)
				<span
					class="tooltip text-lg"
					data-tip="The peak temperature target determines the emissions we can globally still emit. A
			less ambitious target (for example, 2.2 °C) implies the possibility to emit more greenhouse gases."
					>ⓘ</span
				>
				<CustomRange
					bind:value={temperature}
					options={options.temperature.map((d) => Number(d))}
					name="temperature"
				/>
			</div>
			<div class="block">
				Acceptable risk of exceeding global warming limit
				<span
					class="tooltip z-[750] text-lg"
					data-tip="The temperature rise at any level of cumulative emissions has some uncertainties.
					Therefore, if you want to be sure to remain within a given temperature level (small risk), you will need to shrink the budget even more."
					>ⓘ</span
				>
				<CustomRange
					bind:value={exceedanceRisk}
					options={options.exceedanceRisk.map((d) => Number(d))}
					name="risk"
				/>
			</div>
			<div class="block">
				Reduction of non-CO<sub>2</sub> emissions
				<span
					class="tooltip z-[750] text-lg"
					data-tip="Not only CO₂, but also other gases play a role in the global emissions trajectory. Setting this slider to low values assumes small reductions in non-CO₂ by 2040, which means that CO₂ has to reduce much more, and vica versa.
							  In the graph to the right, we show all greenhouse gases (CO₂ and non-CO₂), so the green line will barely move if you adjust this slider, as the temperature goal remains fixed.
							  However, this does greatly affect the carbon budget (which is only the CO₂ part) in the top-left corner of your screen."
					>ⓘ</span
				>
				<CustomRange
					bind:value={nonCO2red}
					options={options.nonCO2red.map((d) => Number(d))}
					name="nonCO2red"
				/>
			</div>
			<p><i>How do we spend these emissions over time is determined by:</i></p>
			<div class="block">
				End-of-century negative emissions
				<span
					class="tooltip text-lg"
					data-tip="A major influence on the shape of the global pathway is the assumption on the amount of negative emissions.
					More negative emissions (slider to the right) gives us some slack in the coming decades, and vice versa."
					>ⓘ</span
				>
				<CustomRange
					bind:value={negativeEmissions}
					options={options.negativeEmissions.map((d) => Number(d))}
					name="negEmis"
				/>
			</div>
			<div>
				Timing of early-century mitigation
				<span
					class="tooltip text-lg"
					data-tip="Analogous to IPCC WGIII scenarios, we distinguish global emission pathways with delayed (i.e., near-similar emissions up to 2030) and immediate action. Delayed action is infeasible with a temperature target of 1.5 °C, so identical data will be shown in that case."
					>ⓘ</span
				>
				<CategoryPicker bind:value={timing} options={options.timing} name="timing" />
			</div>
		</div>
	</div>
</div>
