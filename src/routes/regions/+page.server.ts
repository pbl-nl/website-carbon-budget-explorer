import { borders } from '$lib/server/db/data';
import { listRegions } from '$lib/api';

export async function load() {
	const regionIsos = await listRegions();
	const regions = borders.addNames(regionIsos.map((ISO) => ({ ISO })));
	return { regions };
}
