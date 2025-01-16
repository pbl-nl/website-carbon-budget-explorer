<script lang="ts">
	
	interface Props {
		value: string;
		// TODO allow options to have a value or a label and value
		options: number[];
		name: string;
	}

	let { value = $bindable(), options, name }: Props = $props();

	type ChangeEvent = Event & {
		currentTarget: EventTarget & HTMLInputElement;
	};

	function updateValue(event: ChangeEvent) {
		value = options[event.currentTarget.valueAsNumber].toString();
	}

	let len = $derived(options.length);
	let valIndex = $derived(options.indexOf(parseFloat(value)));
	// when sliding all intermediate values are also fetched
	// TODO could only fetch the value when the slider is released
</script>

<div>
	<div class="flex flex-row gap-2">
		<input
			type="range"
			class="range range-accent range-xs"
			{name}
			min="0"
			max={len - 1}
			step="1"
			value={valIndex}
			onchange={updateValue}
		/>
	</div>
	<div class="flex w-full justify-between px-2 text-xs">
		<!-- TODO make low/high settable to numbers/strings -->
		{#each options as option, index}
			<span class={index === valIndex ? 'font-extrabold' : ''}>{option}</span>
		{/each}
	</div>
</div>
