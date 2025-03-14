import type { PageServerLoad } from '../global/$types';
import {
	globalPathway,
	currentPolicy,
	historicalEmissions,
	ndc,
	netzero,
	globalPathwayOptions,
	pathwayQueryFromSearchParams,
	budget,
	gap
} from '$lib/api';

export const load = (async ({ url }: { url: URL }) => {
	const choices = await globalPathwayOptions();
	const query = pathwayQueryFromSearchParams(url.searchParams, choices);

	const pathway = await globalPathway(url.search);
	const curPol = await currentPolicy();
	const ndc_ = await ndc();

	const result = {
		pathway,
		historicalEmissions: await historicalEmissions(),
		currentPolicy: curPol,
		ndc: ndc_,
		netzero: await netzero(),
		gap: await gap(url.search)
	};
	// TODO many rows in result have same year, so could be optimised for size
	return {
		pathway: {
			query,
			choices
		},
		global: {
			budget: await budget(url.search)
		},
		result
	};
}) satisfies PageServerLoad;
