<script lang="ts">
	import logo from '$lib/logo.svg';
	export const prerender = true;
</script>

<main class="container mx-auto flex h-full w-4/5 flex-col items-stretch justify-around">
	<div class="flex h-2/3 flex-row items-center justify-around">
		<div class="flex flex-col items-end gap-6">
			<div class="flex flex-row items-center gap-8">
				<!-- Logo -->
				<img src={logo} class="color-filter h-36 xl:h-64" alt="Logo for Carbon Budget Explorer" />
				<div class="text-4xl font-bold xl:text-6xl">
					<p>Carbon</p>
					<p>Budget</p>
					<p>Explorer</p>
				</div>
			</div>
			<h2 class="mb-6 text-3xl italic">Exploring fair climate policy in three steps</h2>
		</div>

		<div class="flex flex-col">
			<div class="">
				<ol>
					<li class="mb-1 flex flex-row">
						<h3
							class="z-50 h-12 w-12 rounded-full bg-primary pt-2 text-center text-xl font-semibold text-white"
						>
							1.
						</h3>
						<div class="-ml-6 flex-1 -skew-x-[20deg] rounded bg-neutral p-4 px-10 opacity-60">
							<h3 class="mb-2 text-xl font-semibold text-white">Set global targets</h3>
							<p class="text-white">Defining the global carbon budget and emissions pathway</p>
						</div>
					</li>
					<li class="mb-1 flex flex-row items-start">
						<h3
							class="z-50 h-12 w-12 rounded-full bg-primary pt-2 text-center text-xl font-semibold text-white"
						>
							2.
						</h3>
						<div class="-ml-6 flex-1 -skew-x-[20deg] rounded bg-neutral p-4 px-10 opacity-60">
							<h3 class="mb-2 text-xl font-semibold text-white">
								Choose your effort-sharing principle
							</h3>
							<p class="text-white">Implicating each country's "fair" emissions</p>
						</div>
					</li>
					<li class="mb-1 flex flex-row items-start">
						<h3
							class="z-50 h-12 w-12 rounded-full bg-primary pt-2 text-center text-xl font-semibold text-white"
						>
							3.
						</h3>
						<div class="-ml-6 flex-1 -skew-x-[20deg] rounded bg-neutral p-4 px-10 opacity-60">
							<h3 class="mb-2 text-xl font-semibold text-white">
								Observe individual country results
							</h3>
							<p class="text-white">Indicating the pathway for each country in more detail</p>
						</div>
					</li>
				</ol>
			</div>
		</div>
	</div>

	<!-- text -->
	<div class="">
		<!-- <h2>What is fair climate action?</h2> -->
		<p>
			Many countries commit to rapid climate action, but their ambitions are not enough to reach the
			Paris goals. It is not trivial to define which countries should do more. This is a matter of
			fairness. But what is fair in this context? Should rich countries mitigate more, because they
			have the means to do so? Or the countries that have emitted a lot in the past? Clearly, there
			is no single answer, because it depends on what you think is fair. However, these principles
			can be quantified. The Carbon Budget Explorer allows navigating through the implications of
			different views on fairness.
		</p>
	</div>

	<a class="btn-primary btn-lg btn w-4/5 self-center" href="/global"> Start exploring &raquo; </a>
</main>

<style>
	.color-filter {
		filter: invert(11%) sepia(6%) saturate(127%) hue-rotate(314deg) brightness(101%) contrast(80%);
	}
</style>
