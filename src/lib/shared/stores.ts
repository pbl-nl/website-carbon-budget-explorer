// From: https://www.youtube.com/watch?v=sFEKQt5GqYQ&t=85s
import { writable } from 'svelte/store';

// https://stackoverflow.com/a/61300826/2933427
export const createWritableStore = (key: string, startValue: any): any => {
	const { subscribe, set } = writable(startValue);

	return {
		subscribe,
		set,
		// TODO consider using sessionstorage instead (clears when browser tab closed)
		useLocalStorage: () => {
			const json = localStorage.getItem(key);
			if (json) {
				set(JSON.parse(json));
			}

			subscribe((current) => {
				localStorage.setItem(key, JSON.stringify(current));
			});
		}
	};
};

// tour
export const tour = createWritableStore('tour', { completed: false });
