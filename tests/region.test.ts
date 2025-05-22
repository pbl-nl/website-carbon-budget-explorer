import { expect, test } from '@playwright/test';

/**
 * Run me with
 * ```
 * # Enable test by replacing 'test.skip' with 'test'
 * mkdir -p screenshots
 * npx playwright test --reporter html tests/region.test.ts
 * # Add --headed to see the browser being controlled
 * # Takes about 3.1 minutes on my machine
 * ```
 *
 * Look at screenshots/ folder for screenshots of each region page.
 * Use `npx playwright show-report` for test results.
 */
test('Renders region pages', async ({ page }) => {
	test.setTimeout(3600_000); // 1 hour

	// Fetch list of regions
	await page.goto('/map?allocTime=2030');
	await page.getByText('Select country ▼').click();

	const noncountryRegions = await page.getByLabel('Regions').evaluate((regionsdiv) => {
		return Array.from(regionsdiv.querySelectorAll('a')).map((a) => a.ariaLabel!);
	});
	const countries = await page.getByLabel('Countries').evaluate((regionsdiv) => {
		return Array.from(regionsdiv.querySelectorAll('a')).map((a) => a.ariaLabel!);
	});
	const regions = noncountryRegions.concat(countries);

	expect(regions).not.toHaveLength(0);

	// Close region list
	await page.getByText('Select country ▼').click();

	for (const region of regions) {
		await test.step(
			region,
			async () => {
				await page.getByText('Select country ▼').click();
				await page.getByRole('link', { name: region, exact: true }).click();
				await expect(page).toHaveURL(new RegExp(`/regions/${encodeURIComponent(region)}`), {
					timeout: 20_000
				});

				const path = `screenshots/${region}.png`;
				await page.screenshot({ path });

				await page.getByRole('heading', { name: 'Global budget' });
				await page.getByRole('link', { name: 'Back to map' }).click();
				await expect(page).toHaveURL(new RegExp(`/map`), {
					timeout: 20_000
				});
			},
			{ timeout: 30_000 }
		);
	}
});
