import type { PageLoad } from './$types';
import { searchParam } from '$lib/searchparam';
import {
	budget,
	effortSharingReductions,
	effortSharings,
	globalPathway,
	pathwayQueryFromSearchParams
} from '$lib/api';
import type { principles } from '$lib/principles';

export const load: PageLoad = async ({ params, data, url, fetch }) => {
	const region = params.region;
	const pathwayQuery = pathwayQueryFromSearchParams(url.searchParams, data.pathway.options);
	const pathway = {
		query: pathwayQuery,
		...data.pathway
	};

	// TODO validate region, check that file exists
	// TODO make single api call
	const effortSharing = await effortSharings(region, url.search, fetch);
	const reductions = await effortSharingReductions(region, url.search, fetch);

	let initialEffortSharingName = searchParam<keyof typeof principles>(
		url,
		'effortSharing',
		'PC' // When no effort sharing is selected on prev page, use per capita as default
	);
	if (!(initialEffortSharingName in effortSharing)) {
		// If selected principle does not have data for region, fallback to PC
		if ('PC' in effortSharing) {
			initialEffortSharingName = 'PC';
		} else {
			initialEffortSharingName = Object.keys(effortSharing)[0] as keyof typeof principles;
			// TODO handle when no effort sharing data is available
		}
	}

	const global = {
		...data.global,
		pathway: await globalPathway(url.search, fetch),
		budget: await budget(url.search, fetch)
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
