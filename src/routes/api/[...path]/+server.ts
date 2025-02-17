import { API_URL } from '$lib/config';
import { LRUCache } from 'lru-cache';
import type { RequestHandler } from './$types';

const cache = new LRUCache<string, Uint8Array>({
	maxSize: 1 * 1024 * 1024 * 1024, // 1Gb
	sizeCalculation: (v) => v.byteLength
});

// Poormans cached reverse proxy for /api/* to Python ws
export const GET: RequestHandler = async ({ params, url }) => {
	const path = params.path;
	const localUrl = API_URL + '/' + path + url.search;
	const cached = cache.get(localUrl);
	if (cached !== undefined) {
		return new Response(cached, {
			headers: {
				'content-type': 'application/json'
			}
		});
	}
	const response = await fetch(localUrl);
	if (!response.ok) {
		return response;
	}
	const content = await response.bytes();
	cache.set(localUrl, content);
	// Cannot reuse response as it's already consumed, so make new response
	return new Response(content, {
		headers: {
			'content-type': 'application/json'
		}
	});
};
