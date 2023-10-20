import { describe, test, expect, beforeAll } from 'vitest';

test('1+1', () => {
	expect(1 + 1).toBe(2);
});

// import { mount_data, open_dataset, open_pyodide, slice } from './xarray';
// import type { PyodideInterface } from 'pyodide';

// TODO: keeping this around so we can reuse some of it for
// testing the new flask backend

/*

The __tests__/dummy.nc was created with

```python
import xarray as xr

ds = xr.Dataset({

}, coords={
    'Temperature':['1.5 deg', '1.7 deg', '2.0 deg']
})

ds.to_netcdf('__tests__/dummy.nc')
```

 */
// const testnc = '__tests__/dummy.nc';

// describe('open_dataset', () => {
// 	let ds: any;
// 	let pyodide: PyodideInterface;
// 	beforeAll(async () => {
// 		pyodide = await open_pyodide();
// 		await mount_data('__tests__', pyodide);
// 		ds = await open_dataset(testnc, pyodide);
// 	});

// 	describe('ds.coords', () => {
// 		test('keys()', () => {
// 			const keys = ds.coords.keys();
// 			const value = Array.from(keys[Symbol.iterator]());
// 			expect(value).toEqual(['Temperature']);
// 		});

// 		describe('.Temperature', () => {
// 			let coord: any;

// 			beforeAll(async () => {
// 				coord = ds.Temperature;
// 			});

// 			test('values', () => {
// 				const values = coord.values.tolist().toJs();
// 				expect(values).toEqual(['1.5 deg', '1.7 deg', '2.0 deg']);
// 			});

// 			test('dims', () => {
// 				const values = coord.dims.toJs();
// 				expect(values).toEqual(['Temperature']);
// 			});

// 			test.each([
// 				{
// 					indexer: undefined,
// 					expected: ['1.5 deg', '1.7 deg', '2.0 deg']
// 				}
// 			])('sel($indexer)', ({ indexer, expected }) => {
// 				const values = coord.sel(indexer).values.tolist().toJs();
// 				expect(values).toEqual(expected);
// 			});

// 			test('isel(Temperature=slice(1,3)', () => {
// 				const Temperature = slice(pyodide, 1, 3);
// 				const values = coord.isel
// 					.callKwargs({
// 						Temperature
// 					})
// 					.values.tolist()
// 					.toJs();
// 				const expected = ['1.7 deg', '2.0 deg'];
// 				expect(values).toEqual(expected);
// 			});

// 			test.each([
// 				{
// 					indexer: [0, 2],
// 					expected: ['1.5 deg', '2.0 deg']
// 				}
// 			])('isel(Temperature=$indexer)', ({ indexer, expected }) => {
// 				const values = coord.isel
// 					.callKwargs({
// 						Temperature: indexer
// 					})
// 					.values.tolist()
// 					.toJs();
// 				expect(values).toEqual(expected);
// 			});
// 		});
// 	});
// });
