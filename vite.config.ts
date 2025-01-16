import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		// Exclude /tests/ as it contains playwright tests
		include: ['**/__tests__/**/*.?(c|m)[jt]s?(x)', 'src/**/?(*.){test,spec}.?(c|m)[jt]s?(x)']
	}
});
