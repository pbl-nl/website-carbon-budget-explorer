export interface SpatialMetric {
	ISO: string;
	value: number;
}

export interface NamedSpatialMetric extends SpatialMetric {
	name: string;
}

export interface NamedRegion {
	ISO: string;
	name: string;
}

export interface TemnporalMetric {
	Time: number;
	value: number;
}
