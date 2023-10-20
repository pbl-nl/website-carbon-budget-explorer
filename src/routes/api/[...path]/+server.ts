import { API_URL } from '$lib/api';
import type { RequestHandler } from './$types';

// Poormans reverse proxy for /api/* to Python ws
export const GET: RequestHandler = async ({ params, url }) => {
	const path = params.path;
	return fetch(API_URL + '/' + path + '?' + url.search);
};
