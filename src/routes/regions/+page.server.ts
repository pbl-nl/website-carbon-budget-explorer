import { listRegions } from '$lib/api';

export async function load() {
	const regions = await listRegions();
	return { regions };
}
