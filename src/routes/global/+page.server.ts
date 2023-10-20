import type { PageServerLoad } from '../global/$types';
import {
	pathwayCarbon,
	currentPolicy,
	historicalCarbon,
	ndc,
	netzero,
	pathwayChoices,
	pathwayQueryFromSearchParams,
	pathwayStats
} from '$lib/api';

export const load = (async ({ url }: { url: URL }) => {
	const choices = await pathwayChoices();
	const query = pathwayQueryFromSearchParams(url.searchParams, choices);

	const pathway = await pathwayCarbon(url.search);
	const curPol = await currentPolicy();
	const ndc_ = await ndc();

	const emissionGap =
		curPol.find((d) => d.time === 2030)!.mean - pathway.find((d) => d.time === 2030)!.mean;
	const ambitionGap =
		ndc_.find((d) => d.time === 2030)!.mean - pathway.find((d) => d.time === 2030)!.mean;

	const result = {
		pathwayCarbon: pathway,
		pathwayStats: await pathwayStats(url.search),
		historicalCarbon: await historicalCarbon(),
		currentPolicy: curPol,
		ndc: ndc_,
		netzero: await netzero(),
		ambitionGap,
		emissionGap
	};
	// TODO many rows in result have same year, so could be optimised for size
	return {
		pathway: {
			query,
			choices
		},
		result
	};
}) satisfies PageServerLoad;
