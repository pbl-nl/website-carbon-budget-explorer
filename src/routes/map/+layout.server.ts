import { borders, listRegions } from '$lib/api';

import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async () => {
	const regions = await listRegions();
	const borders_as_geojson = await borders();

	return {
		borders: borders_as_geojson,
		regions
	};
};
