import { expect, test } from '@playwright/test';

test('index page has expected link', async ({ page }) => {
	await page.goto('/');
	await expect(page.getByRole('link', { name: /Start exploring/ })).toBeVisible();
});
