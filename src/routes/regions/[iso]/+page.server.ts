import type { PageServerLoad } from './$types';
import { currentPolicy, historicalCarbon, indicators, pathwayChoices, regionInfo } from '$lib/api';
import { extent } from 'd3';

// TODO figure out when pathway query in url.searchparams is changed
// then this load method is not called, but only ./+page.ts:load is called

export const load: PageServerLoad = async ({ params }) => {
	const iso = params.iso;

	const choices = await pathwayChoices();
	const info = await regionInfo(iso);
	const hist = await historicalCarbon(iso, 1850, 2021);
	const indicators_ = await indicators(iso);
	if (indicators_.ndcAmbition !== null) {
		// Country has historical ndc and probably also curpol and netzero
		// TODO fetch ndc, curpol, netzero and plot
	}

	const global = {
		historicalCarbon: await historicalCarbon(),
		currentPolicy: await currentPolicy()
	};

	const r = {
		info,
		pathway: {
			choices
		},
		historicalCarbon: {
			data: hist,
			extent: extent(hist, (d) => d.value) as [number, number]
		},
		indicators: indicators_,
		global
	};
	return r;
};
