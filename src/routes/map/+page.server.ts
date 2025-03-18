import { searchParam } from '$lib/searchparam';
import {
	currentPolicy,
	fullCenturyBudgetSpatial,
	historicalEmissions,
	globalPathway,
	globalPathwayOptions,
	pathwayQueryFromSearchParams,
	budget
} from '$lib/api';
import type { BudgetSpatial } from '$lib/api';
import type { allocationMethods } from '$lib/allocationMethods';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url }: { url: URL }) => {
	const options = await globalPathwayOptions();
	const pathwayQuery = pathwayQueryFromSearchParams(url.searchParams, options);
	const pathway = {
		query: pathwayQuery,
		options
	};

	const selectedAllocationMethod = searchParam<undefined | keyof typeof allocationMethods>(
		url,
		'allocationMethod',
		'PCC'
	);

	const selectedAllocationTime = searchParam<string>(url, 'allocTime', '2030');

	let rawMetrics: BudgetSpatial = {
		data: [],
		domain: [0, 1]
	};
	if (selectedAllocationMethod !== undefined) {
		rawMetrics = await fullCenturyBudgetSpatial(
			selectedAllocationTime,
			selectedAllocationMethod,
			url.search
		);
	}

	const metrics = {
		data: rawMetrics.data,
		domain: rawMetrics.domain
	};

	const global = {
		historicalEmissions: await historicalEmissions(),
		pathway: await globalPathway(url.search),
		currentPolicy: await currentPolicy(),
		budget: await budget(url.search)
	};

	const data = {
		pathway,
		allocationMethod: selectedAllocationMethod,
		metrics,
		global
	};
	return data;
};
