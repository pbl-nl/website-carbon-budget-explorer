import type { PageLoad } from './$types';
import { searchParam } from '$lib/searchparam';
import {
	effortSharingReductions,
	effortSharings,
	pathwayCarbon,
	pathwayQueryFromSearchParams,
	pathwayStats
} from '$lib/api';
import type { principles } from '$lib/principles';

export const load: PageLoad = async ({ params, data, url, fetch }) => {
	const iso = params.iso;
	const pathwayQuery = pathwayQueryFromSearchParams(url.searchParams, data.pathway.choices);
	const pathway = {
		query: pathwayQuery,
		stats: await pathwayStats(url.search, fetch),
		...data.pathway
	};
	const initialEffortSharingName = searchParam<keyof typeof principles>(
		url,
		'effortSharing',
		'PC' // When no effort sharing is selected on prev page, use per capita as default
	);

	// TODO validate iso, check that file exists
	// TODO make single api call
	const effortSharing = await effortSharings(iso, url.search, fetch);
	const reductions = await effortSharingReductions(iso, url.search, fetch);

	const global = {
		...data.global,
		pathwayCarbon: await pathwayCarbon(url.search, fetch)
	};

	return {
		...data,
		pathway,
		initialEffortSharingName,
		effortSharing,
		reductions,
		global
	};
};
