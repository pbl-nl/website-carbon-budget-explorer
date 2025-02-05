<script lang="ts">
	import QA from '$lib/QA.svelte';

	export const prerender = false;
</script>

<!-- Sidebar -->
<div class="flex h-full gap-4 rounded bg-primary">
	<div class="items-between flex h-full w-1/5 flex-col rounded bg-primary">
		<div class="card card-compact">
			<div class="card-body prose">
				<h2 class="card-title text-white">About</h2>
				<ul class="not-prose m-2 list-inside list-disc">
					<li class="text-lg font-semibold text-white"><a href="#scientific">Introduction</a></li>
					<li class="text-lg font-semibold text-white"><a href="#societal">Scientific basis</a></li>
					<li class="text-lg font-semibold text-white"><a href="#technology">Other</a></li>
				</ul>
			</div>
		</div>
		<div class="card card-compact mt-auto">
			<div class="card-body prose">
				<h2 class="card-title text-white">More information</h2>
				<p class="text-white">
					This tool was developed by the <a
						href="https://www.esciencecenter.nl/"
						target="_blank"
						rel="noopener
					noreferrer"
						class="text-white">Netherlands eScience Center</a
					>
					in collaboration with the
					<a
						href="https://www.pbl.nl/en"
						target="_blank"
						rel="noopener noreferrer"
						class="text-white">Environmental Assessment Agency (PBL)</a
					>, in the context of the
					<a
						href="https://www.ecemf.eu/about/"
						target="_blank"
						rel="noopener noreferrer"
						class="text-white">ECEMF</a
					>
					and
					<a
						href="https://www.elevate-climate.org/"
						target="_blank"
						rel="noopener noreferrer"
						class="text-white">ELEVATE</a
					>
					projects. For more information you can contact dr.
					<a
						href="https://www.pbl.nl/over-het-pbl/medewerkers/mark-dekker"
						target="_blank"
						class="text-white"
						rel="noopener noreferrer">Mark Dekker.</a
					>
					<br /><br />© 2023 Planbureau voor de Leefomgeving and Netherlands eScience Center.
					<img src="/logo_pbl.png" alt="logo_pbl" width="200" />
					<img src="/logo_ecemf.png" alt="logo_ecemf" width="200" />
					<img src="/logo_elevate.png" alt="logo_elevate" width="200" />
					<img src="/netherlands-escience-center-logo-DIAP.png" alt="logo_escience" width="200" />
				</p>
			</div>
		</div>
	</div>
	<!-- Main panel -->
	<main class="relative max-h-full flex-1 overflow-auto bg-base-100 p-4">
		<!-- TODO update page -->
		<div class="prose absolute ml-4 max-w-[60%]">
			<h1>Frequently asked questions</h1>
			<section>
				<h2 id="intro">Introduction</h2>
				<QA question="What is the goal of this explorer?">
					The goal is to inform everyone about the consequences of one's view on fairness and
					requirements of climate targets. The calculations in this tool act as a 'mirror' to
					reflect on how the ambition gap can be closed and evaluate NDCs in light of fairness.
				</QA>
				<QA question="How should I interpret these results?">
					The results are all about allocating emissions to countries based on various principles of
					fairness. The tool focuses on the mitigation part of climate change. This exercise is
					therefore also referred to as 'burden-sharing' or 'effort-sharing' in the race to climate
					neutrality: it describes how the burden of reducing emissions can be shared among
					countries in a fair manner.
				</QA>
				<QA question="What perspectives of fairness are considered here?">
					Three core principles of fairness are identified in scientific literature: (1)
					responsibility, taking into account historical emissions, (2) capability, emphasizing a
					country's financial and institutional means to implement mitigation, and (3) equality,
					where person on Earth gets equal allocations. For comparison and as a reference, we
					include the principle of continuity. These principles are subsequently quantified using
					mathematical formula: so-called allocation methods such as 'per capita' and 'ability to
					pay'.
				</QA>
				<QA question="How does this relate to just transitions?">
					Emissions are indicative for the general burden of climate policy, but clearly not the
					only aspect of just transitions. The costs of climate policy and welfare, loss and damages
					due to climate change, negative emissions, various sustainable development goals (SDGs)
					are important considerations of a just transition to climate neutrality, reaching far
					beyond emission allocations only. We hope this tool is a step in the right direction and
					hope to complement this further in the future.
				</QA>
			</section>
			<section>
				<h2 id="scientific">Scientific basis</h2>
				<QA question="What is the global carbon budget?">
					The global carbon budget, or remaining carbon budget (RCB) is the maximum amount of CO<sub
						>2</sub
					>
					that can be emitted to remain with a certain maximum level of warming. Although conceptually
					relatively simple, there are many uncertainties involved. These uncertainties are captured
					by the 'Risk' slider in this tool, which captures the various estimations of the temperature
					response to CO<sub>2</sub>. Note that this budget is expressed in CO<sub>2</sub>
					emissions, while most figures in this tool are computed for all greenhouse gases. It only makes
					sense to talk about a budget in terms of cumulative CO<sub>2</sub> emissions, because CO<sub
						>2</sub
					>
					remains in the atmosphere for a long time, while other greenhouse gases are mostly short-lived
					and filtered out quickly from the atmosphere, so it matters when exactly these greenhouse gases
					are emitted. The global carbon budget numbers are taken from
					<a
						href="https://essd.copernicus.org/articles/15/2295/2023/"
						target="_blank"
						rel="noopener noreferrer">Forster et al. (2023)</a
					>, who summarize updates of the WGI and WGIII reports of the IPCC, and updates of climate
					emulators. This update involved more stringent numbers of the global carbon budget than
					earlier reported. The authors also wrote a
					<a
						href="https://www.carbonbrief.org/guest-post-what-the-tiny-remaining-1-5c-carbon-budget-means-for-climate-policy/"
						target="_blank"
						rel="noopener noreferrer">blog</a
					> on Carbon Brief about this, going in more detail into the topic.
				</QA>
				<QA question="How did you construct the global pathway?">
					The global carbon budget (in turn dependent on the slider settings) is used to filter
					climate mitigation scenarios from the IPCC Sixth Assessment Report
					<a href="https://zenodo.org/records/5886912" target="_blank" rel="noopener noreferrer"
						>scenario database</a
					>, which is a collection of over 2000 long-term mitigation pathways. The filtered pathways
					that are associated with the budget are used to define the curvature of the CO<sub>2</sub>
					part of the global emissions pathway, for different values of negative emissions. The non-CO<sub
						>2</sub
					>
					part of the global emissions pathway is based on estimations of
					<a
						href="https://essd.copernicus.org/articles/15/2295/2023/"
						target="_blank"
						rel="noopener noreferrer">Forster et al. (2023)</a
					>. The negative emissions slider is based on percentiles of 2100 emissions in IPCC AR6
					WGIII scenarios.
				</QA>
				<QA question="How did you do the allocations?">
					There are multiple methodologically distinct ways of allocating global emissions. We
					allocate global emissions year by year. For example, the 'per capita' allocation method
					distributes global emissions of a given year based on population distributions. This is
					similar to the temporal allocations done in
					<a
						href="https://link.springer.com/article/10.1007/s10584-019-02368-y"
						target="_blank"
						rel="noopener noreferrer">Van den Berg et al. (2019)</a
					>., for example, but different from the budget-based (and subsequent linear projection of)
					allocation in
					<a
						href="https://newclimate.org/resources/publications/what-is-a-fair-emissions-budget-for-the-netherlands"
						target="_blank"
						rel="noopener noreferrer">Fekete et al. (2022)</a
					>.
				</QA>
				<QA question="What data sources did you use?">
					For future population and GDP data, we used the Shared-Socioeconomic Pathways database,
					containing five socioeconomic scenario projections. For past population data, we used UN
					population data. For historical emissions, we used the PRIMAP database. For data on the
					global carbon budget, non-CO<sub>2</sub> and global emission pathways, we used
					<a
						href="https://essd.copernicus.org/articles/15/2295/2023/"
						target="_blank"
						rel="noopener noreferrer">Forster et al. (2023)</a
					>
					and the AR6
					<a href="https://zenodo.org/records/5886912" target="_blank" rel="noopener noreferrer"
						>scenario database</a
					>. For NDC data, we use the PBL Climate Pledge NDC tool.
				</QA>
				<QA question="What are these allocation methods?">
					Below, we briefly describe the methods one-by-one. For more details, the reader is
					referred to earlier work by
					<a
						href="https://link.springer.com/article/10.1007/s10584-019-02368-y"
						target="_blank"
						rel="noopener noreferrer">Van den Berg et al. (2019)</a
					>.
					<br />
					<br />The 'Per Capita' method uses a country's population share in the global population
					and allocates future emissions accordingly. Naturally, the socio-economic scenario affects
					this method. All five SSPs are used in our analysis.
					<br />
					<br />
					'Grandfathering' is a method that preserves current emission fractions. In other words, all
					countries reduce their emissions proportional to their current share.
					<br />
					<br />
					The 'Per Capita Convergence' method starts as Grandfathering, but converges over time to a
					Per Capita basis. An additional important parameter here is the year at which this convergence
					completes.
					<br />
					<br />
					The 'Ability to Pay' method allocates emissions inversely related to the GDP per capita of
					countries. Also this method is dependent on the socio-economic scenario.
					<br />
					<br />
					The 'Equal Cumulative Per Capita' method computes the total budget (past plus future) that
					a country would obtain based on their (past plus future) population fractions, and then subtracts
					from this the already spent emissions in the past.
					<br />
					<br />
					The 'Greenhouse Development Rights' method is, in the short run, based on a
					<a
						href="https://calculator.climateequityreference.org/"
						target="_blank"
						rel="noopener noreferrer">Responsibility-Capability Index</a
					>, and in the long run based on GDP per capita (similar to Ability to Pay).
				</QA>
				<QA question="Why are there different absolute NDC values shown in the country graph?">
					When NDCs area published by countries, they are expressed in relative terms (e.g. 30 %
					reduction in 2030 compared to 1990). The absolute values are calculations that depend on
					the historical and baseline emission data used. We show two versions: one based on the
					data we use for the Carbon Budget Explorer (Jones et al., 2021), and one based on the data
					used in the
					<a
						href="https://themasites.pbl.nl/o/climate-ndc-policies-tool/"
						target="_blank"
						rel="noopener noreferrer">PBL NDC tool</a
					>
					(PRIMAP historical data).
					<br />
					<br />
					These values are only an indication. When precise NDC data is needed, it is better to refer
					to the official NDC documents.
				</QA>
				<QA question="Why are there no NDCs for European Member States?">
					European Member States have a joint NDC, which is to reduce GHG emissions by at least 55 %
					by 2030 compared to 1990 levels. This is a shared goal for the EU27, and therefore no
					individual NDCs are available for European Member States.
					<br />
					<br />
					The allocation of emission reductions to each Member State is determined via several Directives
					(ETS, ESR and others). You can find
					<a
						href="https://data.consilium.europa.eu/doc/document/ST-14286-2023-INIT/en/pdf"
						target="_blank"
						rel="noopener noreferrer">more information here.</a
					>
				</QA>
			</section>
			<section>
				<h2 id="other">Other</h2>
				<QA question="How can I contact you?">
					All questions, comments and ideas are welcome. Please contact dr. <a
						href="https://www.pbl.nl/over-het-pbl/medewerkers/mark-dekker"
						target="_blank"
						rel="noopener noreferrer">Mark Dekker</a
					> from the Netherlands Environmental Assessment Agency.
				</QA>
				<QA question="How can I cite this work?">
					For general purposes, feel free to refer to this work as Dekker, M.M. (2023) The Carbon
					Budget Explorer. [Online]. Available: https://www.carbonbudgetexplorer.eu. <br />
					<br /> For scientific purposes, you can refer to the
					<a
						href="https://doi.org/10.21203/rs.3.rs-5023350/v1"
						target="_blank"
						rel="noopener noreferrer">preprint</a
					>
					of this work. It is currently under review.
				</QA>
				<QA question="Will the data and code be publicly available?">
					All data can be downloaded <a
						href="https://doi.org/10.5281/zenodo.12188104"
						target="_blank">from Zenodo</a
					>, including more recent developments. The Python code for the computations can be found
					on
					<a href="https://doi.org/10.5281/zenodo.13640303" target="_blank">Zenodo</a> or
					<a href="https://github.com/imagepbl/EffortSharing/tree/v1.0.0" target="_blank">GitHub</a
					>.
				</QA>
				<QA question="What future updates are expected?">
					The Explorer is constantly in development, by updating NDC or other data, but also in
					terms of layout. If you have any ideas of improvement, please feel free to contact us.
				</QA>
			</section>
		</div>
	</main>
</div>
