import type { PageLoad } from './$types';
import { searchParam } from '$lib/searchparam';
import {
	budget,
	allocationReduction,
	getEmissionsAllocations,
	globalPathway,
	pathwayQueryFromSearchParams
} from '$lib/api';
import type { allocationMethods } from '$lib/allocationMethods';

export const load: PageLoad = async ({ params, data, url, fetch }) => {
	const region = params.region;
	const pathwayQuery = pathwayQueryFromSearchParams(url.searchParams, data.pathway.defaults);
	const pathway = {
		query: pathwayQuery,
		...data.pathway
	};

	// TODO validate region, check that file exists
	const allocationMethod = await getEmissionsAllocations(region, url.search, fetch);
	const reductions = await allocationReduction(region, url.search, fetch);

	let initialAllocationMethod = searchParam<keyof typeof allocationMethods>(
		url,
		'allocationMethod',
		'PC' // When no allocation method is selected on prev page, use per capita as default
	);
	if (!(initialAllocationMethod in allocationMethod)) {
		// If selected allocation method does not have data for region, fallback to PC
		if ('PC' in allocationMethod) {
			initialAllocationMethod = 'PC';
		} else {
			initialAllocationMethod = Object.keys(allocationMethod)[0] as keyof typeof allocationMethods;
			// TODO handle when no allocation data is available
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
		initialAllocationMethod,
		allocationMethod,
		reductions,
		global
	};
};
