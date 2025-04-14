import { defineConfig } from '@playwright/test';

export default defineConfig({
	webServer: {
		command: 'npm run build && npm run preview',
		port: 4173
	},

	testDir: 'tests',
	testMatch: '**/*.@(spec|test).?(c|m)[jt]s?(x)'
});
