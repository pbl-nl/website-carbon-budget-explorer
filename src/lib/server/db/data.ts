import { open_borders } from './borders';

export const dataDir = process.env.CABE_DATA_DIR || 'data';

const bordersPath = dataDir + '/ne_110m_admin_0_countries.geojson';
export const borders = await open_borders(bordersPath);
