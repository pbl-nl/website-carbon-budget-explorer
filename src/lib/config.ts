import { env } from '$env/dynamic/public';

// Sveltkit env type is hardcoded to PUBLIC_, override it
interface Env {
	CABE_API_URL: string | undefined;
}

export const API_URL = (env as unknown as Env).CABE_API_URL ?? 'http://127.0.0.1:5000';
