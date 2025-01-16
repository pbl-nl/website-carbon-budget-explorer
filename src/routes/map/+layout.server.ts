import { borders as bordersDb } from '$lib/server/db/data';
import {
	listRegions} from '$lib/api';

export async function load() {
	const regions = await listRegions();

	const data = {
		borders: bordersDb.geojson,
		regions
	};

	return data;
}
