import { browser } from '$app/environment';
import { LRUCache } from 'lru-cache';
import sizeof from 'object-sizeof';
import { API_URL } from './config';
import type { principles } from './principles';

export interface SpatialMetric {
	Region: string;
	value: number;
}

export interface PathWayQuery {
	temperature: string;
	exceedanceRisk: string;
	negativeEmissions: string;
	timing: string;
	nonCO2red: string;
}

export interface Gap {
	index: number;
	budget: number;
	curPol: number;
	ndc: number;
}

export interface TimeSeriesValue {
	time: number;
	mean: number;
	min: number;
	max: number;
}

// TODO transpose structure: time, mean, min and max arrays as attributes
export interface TimeSeries {
	name: string;
	values: TimeSeriesValue[];
}

/**
 * make pyodide toJs(toJsOpts) return a list of JS object instead of list of Map instances
 */
export const toJsOpts = { dict_converter: Object.fromEntries };
export type UncertainTime = {
	time: number;
	mean: number;
	max: number;
	min: number;
};
export type CertainTime = {
	time: number;
	value: number;
};

export interface BorderProperties {
	ISO_A2_EH: string;
	ISO_A3_EH: string;
	NAME: string;
}

export type BordersCollection = GeoJSON.FeatureCollection<null, BorderProperties>;

export function pathwayQueryFromSearchParams(
	searchParams: URLSearchParams,
	choices: Record<keyof PathWayQuery, string[]>
): PathWayQuery {
	// TODO check each searchParam is in respective choices array
	const temperature = searchParams.get('temperature') ?? choices.temperature[5]; //Math.floor(choices.temperature.length / 2)];
	const exceedanceRisk = searchParams.get('exceedanceRisk') ?? choices.exceedanceRisk[2]; //[Math.floor(choices.exceedanceRisk.length / 2)];
	// TODO when more choices are available use Medium==1 as default
	const negativeEmissions = searchParams.get('negativeEmissions') ?? choices.negativeEmissions[3]; //[Math.floor(choices.negativeEmissions.length / 2)];
	const timing = searchParams.get('timing') ?? choices.timing[1]; //[Math.floor(choices.timing.length / 2)];
	const nonCO2red = searchParams.get('nonCO2red') ?? choices.nonCO2red[2]; //[Math.floor(choices.nonCO2red.length / 2)];
	return {
		temperature,
		exceedanceRisk,
		negativeEmissions,
		timing,
		nonCO2red
	};
}

type Fetch = typeof fetch;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let cache: LRUCache<string, any> | undefined = undefined;
if (!browser) {
	cache = new LRUCache({
		maxSize: 1 * 1024 * 1024 * 1024, // 1Gb
		sizeCalculation: sizeof
	});
}

async function getJSON(path: string, myfetch = fetch) {
	if (browser) {
		return getJSONOnBrowser(path, myfetch);
	}
	return getJSONOnServer(path, myfetch);
}

async function getJSONOnBrowser(path: string, myfetch = fetch) {
	const url = `/api/${path}`;
	const response = await myfetch(url);
	if (!response.ok) {
		console.error(url);
		throw new Error(response.statusText);
	}
	return await response.json();
}

async function getJSONOnServer(path: string, myfetch = fetch) {
	const url = `${API_URL}${path}`;
	const cached = cache?.get(url);
	if (cached !== undefined) {
		return cached;
	}
	const response = await myfetch(url);
	if (!response.ok) {
		console.error(url);
		throw new Error(response.statusText);
	}
	const data = await response.json();
	cache?.set(url, data);
	return data;
}

export async function globalPathwayOptions(): Promise<Record<keyof PathWayQuery, string[]>> {
	const path = '/options/pathway/global';
	return getJSON(path);
}

export async function budget(
	search: string,
	fetch?: Fetch
): Promise<{
	remaining: number;
	relative: number;
}> {
	return getJSON(`/statistics/budget/global${search}`, fetch);
}

export async function gap(search: string, fetch?: Fetch): Promise<Gap> {
	const path = `/statistics/gap/global${search}`;
	return getJSON(path, fetch);
}

export async function globalPathway(search: string, fetch?: Fetch): Promise<UncertainTime[]> {
	// TODO: send data instead of search string?
	// TODO: update search with default choices
	return getJSON(`/timeseries/global/emissions/pathway${search}`, fetch);
}

export async function historicalEmissions(
	region = 'EARTH',
	start = 1990,
	end = 2021
): Promise<CertainTime[]> {
	return getJSON(`/timeseries/${region}/emissions/historical?start=${start}&end=${end}`);
}

export interface Region {
	iso2: string;
	iso3: string;
	name: string;
}

export async function listRegions(): Promise<Region[]> {
	return getJSON(`/regions`);
}

export async function regionInfo(region: string): Promise<Region> {
	return getJSON(`/regions/${region}`);
}

export interface BudgetSpatial<T = SpatialMetric> {
	data: T[];
	domain: [number, number];
}

export async function fullCenturyBudgetSpatial(
	allocationTime: string,
	effortSharing: keyof typeof principles,
	search: string
	// Scenario = 'SSP2',
	// Convergence_year = 2040
): Promise<BudgetSpatial> {
	return getJSON(`/map/${allocationTime}/${effortSharing}${search}`);
}

async function policyPathway(policy: string, Region: string): Promise<UncertainTime[]> {
	return getJSON(`/timeseries/${Region}/policies/${policy}`);
}

export async function currentPolicy(Region = 'EARTH'): Promise<UncertainTime[]> {
	return await policyPathway('CurPol', Region);
}

export async function ndc(Region = 'EARTH'): Promise<UncertainTime[]> {
	return await policyPathway('NDC', Region);
}

export async function netzero(Region = 'EARTH'): Promise<UncertainTime[]> {
	return await policyPathway('NetZero', Region);
}

export async function ndcProjections(region: string): Promise<{
	ndc_inventory: Record<number, [number, number]> | null;
	ndc_jones: Record<number, [number, number]> | null;
}> {
	return getJSON(`/statistics/ndc/projections/${region}`);
}

export async function ndcReductions(region: string): Promise<{ min: number; max: number } | null> {
	return getJSON(`/statistics/ndc/reductions/${region}`);
}

export async function effortSharings(
	region: string,
	search: string,
	fetch: Fetch
): Promise<Record<string, UncertainTime[]>> {
	return getJSON(`/timeseries/${region}/principles${search}`, fetch);
}

export async function effortSharingReductions(
	region: string,
	search: string,
	fetch: Fetch
): Promise<Record<string, Record<number, number>>> {
	return getJSON(`/statistics/reductions/${region}${search}`, fetch);
}

export async function borders(fetch?: Fetch): Promise<BordersCollection> {
	return getJSON('/borders', fetch);
}
