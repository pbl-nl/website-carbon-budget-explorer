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
test.skip('Renders region pages', async ({ page }) => {
	test.setTimeout(600_000); // 10 minutes

	// Fetch list of regions
	await page.goto('/map?allocTime=2030');
	await page.getByText('Select country ▼').click();

	const regions = await page.getByLabel('Regions').evaluate((regionsdiv) => {
		return Array.from(regionsdiv.querySelectorAll('a')).map((a) => a.ariaLabel!);
	});
	expect(regions).not.toHaveLength(0);

	// Close region list
	await page.getByText('Select country ▼').click();

	for (const region of regions) {
		await test.step(
			region,
			async () => {
				await page.getByText('Select country ▼').click();
				await page.getByRole('link', { name: region, exact: true }).click();
				await expect(page).toHaveURL(new RegExp(`/regions/${encodeURIComponent(region)}`));

				const path = `screenshots/${region}.png`;
				await page.screenshot({ path });

				await page.getByRole('heading', { name: 'Global budget' });
				await page.getByRole('link', { name: 'Back to map' }).click();
				await expect(page).toHaveURL(new RegExp(`/map`));
			},
			{ timeout: 2_000 }
		);
	}
});
