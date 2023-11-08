// Add VS Code integration for ?client
// see https://github.com/bluwy/vite-plugin-iso-import
declare module 'svelte-leafletjs?client' {
	import * as all from 'svelte-leafletjs';
	export = all;
}
declare module 'leaflet?client' {
	import * as all from 'leaflet';
	export = all;
}
