import { borders as bordersDb } from '$lib/server/db/data';
import { searchParam } from '$lib/searchparam';
import {
	currentPolicy,
	fullCenturyBudgetSpatial,
	historicalCarbon,
	listRegions,
	pathwayCarbon,
	pathwayChoices,
	pathwayQueryFromSearchParams,
	pathwayStats
} from '$lib/api';
import type { BudgetSpatial } from '$lib/api';
import type { principles } from '$lib/principles';

export async function load({ url }: { url: URL }) {
	const choices = await pathwayChoices();
	const pathwayQuery = pathwayQueryFromSearchParams(url.searchParams, choices);
	const pathway = {
		query: pathwayQuery,
		stats: await pathwayStats(url.search),
		choices
	};

	const selectedEffortSharing = searchParam<undefined | keyof typeof principles>(
		url,
		'effortSharing',
		'PCC'
	);

	const selectedAllocationTime = searchParam<string>(url, 'allocTime', '2021-2100');

	let rawMetrics: BudgetSpatial = {
		data: [],
		domain: [0, 1]
	};
	if (selectedEffortSharing !== undefined) {
		rawMetrics = await fullCenturyBudgetSpatial(selectedAllocationTime, url.search);
	}

	const regions = await listRegions();
	const metrics = {
		data: rawMetrics.data,
		domain: rawMetrics.domain
	};

	const global = {
		historicalCarbon: await historicalCarbon(),
		pathwayCarbon: await pathwayCarbon(url.search),
		currentPolicy: await currentPolicy()
	};

	const data = {
		pathway,
		effortSharing: selectedEffortSharing,
		metrics,
		borders: bordersDb.geojson,
		regions,
		global
	};
	return data;
}
