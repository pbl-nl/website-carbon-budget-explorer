import type { PageServerLoad } from './$types';
import {
	currentPolicy,
	historicalEmissions,
	ndcReductions,
	ndcProjections,
	globalPathWayDefaults,
	globalPathwayOptions,
	listRegions,
	type Region
} from '$lib/api';
import { extent } from 'd3';

// TODO figure out when pathway query in url.searchparams is changed
// then this load method is not called, but only ./+page.ts:load is called

function nestRegions(regions: Region[], region: string) {
	const regionLookup = new Map<string, Region>(regions.map((r) => [r.iso3, r]));
	const info = regionLookup.get(region);
	if (!info) {
		throw new Error(`Region ${region} not found`);
	}
	const countriesOfRegion = info.countries?.map((c) => regionLookup.get(c)!);
	const regionsOfCountry = info.regions?.map((r) => regionLookup.get(r)!);
	return {info, countriesOfRegion, regionsOfCountry};
}

export const load: PageServerLoad = async ({ params }) => {
	const region = params.region;

	const options = await globalPathwayOptions();
	const defaults = await globalPathWayDefaults();
	const regions = await listRegions();
	const {info, countriesOfRegion, regionsOfCountry} = nestRegions(regions, region);
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
			options,
			defaults
		},
		historicalEmissions: {
			data: hist,
			extent: extent(hist, (d) => d.value) as [number, number]
		},
		ndcReduction,
		ndcProjection,
		global,
		countriesOfRegion,
		regionsOfCountry
	};
	return r;
};
