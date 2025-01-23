import { open_borders } from './borders';

// export const dataDir = 'data'
export const dataDir = '/data/DataUpdate_02_2024'

const bordersPath = dataDir + '/ne_110m_admin_0_countries.geojson';

export const borders = await open_borders(bordersPath);
