import type { PageServerLoad } from './$types';
import {
	currentPolicy,
	historicalEmissions,
	globalPathwayOptions,
	regionInfo,
	ndcReductions,
	ndcProjections
} from '$lib/api';
import { extent } from 'd3';

// TODO figure out when pathway query in url.searchparams is changed
// then this load method is not called, but only ./+page.ts:load is called

export const load: PageServerLoad = async ({ params }) => {
	const region = params.region;

	const choices = await globalPathwayOptions();
	const info = await regionInfo(region);
	const hist = await historicalEmissions(region, 1850, 2021);
	const ndcReduction = await ndcReductions(region);
	const ndcProjection = await ndcProjections(region);
	if (ndcReduction !== null) {
		// Country has historical ndc and probably also curpol and netzero
		// TODO fetch ndc, curpol, netzero and plot
	}

	const global = {
		historicalEmissions: await historicalEmissions(),
		currentPolicy: await currentPolicy()
	};

	const r = {
		info,
		pathway: {
			choices
		},
		historicalEmissions: {
			data: hist,
			extent: extent(hist, (d) => d.value) as [number, number]
		},
		ndcReduction,
		ndcProjection,
		global
	};
	return r;
};
