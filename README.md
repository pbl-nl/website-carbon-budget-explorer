# Carbon Budget Explorer (CABE)

[![CI](https://github.com/carbon-budget-explorer/cabe/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/carbon-budget-explorer/cabe/actions/workflows/ci.yml)

Web application to explore carbon budgets

The web application is written with [SveltKit](https://kit.svelte.dev/).

## Data requirements and configuration

Should have the following data files:

1. `{CABE_DATA_DIR} / "ne_110m_admin_0_countries.geojson"` - can be downloaded with `npm run download:borders` and move downloaded file to CABE_DATA_DIR directory.
1. `{CABE_DATA_DIR} / "xr_policyscen.nc"`- Policy scenario data
1. `{CABE_DATA_DIR} / {CABE_START_YEAR} / "xr_dataread.nc"` - Global data
1. `{CABE_DATA_DIR} / {CABE_START_YEAR} / {CABE_ASSUMPTIONSET} / "Allocations" / "xr_alloc_{ISO}.nc"` - Region specific data
1. `{CABE_DATA_DIR} / {CABE_START_YEAR} / {CABE_ASSUMPTIONSET} / "Aggregated_files" / "xr_alloc_{YEAR}.nc"` - Aggregated data

The `CABE_DATA_DIR` variable is the path to the data directory.
The `CABE_START_YEAR` variable is the start year of the allocation.
The `CABE_ASSUMPTIONSET` variable encodes assumptions on which gases are included (GHG or CO2_only) and land use (included/excluded).
The `ISO` variable is the 3 letter ISO code of the region.
The `YEAR` variable is the year of the allocation.

The `CABE_` variables are defined in the `.env` file.
See [.env.example](.env.example) file for an example.
To run the application the `.env` file is required.

## API service

The API web service reads the NetCDF file and returns the data as JSON which is used in the web application.

It is written in Python using [Flask](https://flask.palletsprojects.com/) and [xarray](https://xarray.dev/).

Python dependencies can be installed with

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The web service can be started with

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 'ws:app'
```

(Add `--reload` argumment to reload on Python file changes)

In Windows gunicorn might not work. Then use waitress.

```shell
pip install waitress
waitress-serve --listen=127.0.0.1:5000 ws:app
```

## Developing

You'll need [node.js](https://nodejs.org/en) (v22 or greater) to run a local development server.
Once you've created a project and installed dependencies with `npm install`, start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Formatting & linting

The code is formatted with [Prettier](https://prettier.io/) using

```bash
npm run format
```

The code can be linted, using Prettier and eslint, with

```bash
npm run lint
```

The code can be checked with

```bash
npm run check
```

## Testing

The unit test can be run with

```bash
npm run test:unit
```

For coverage, run

```bash
npm run test:unit -- run --coverage
```

The end-to-end test can be run with

```bash
npm run test
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can run the production build with

```bash
node --env-file=.env build/index.js
```

The web application server expects the Python web service to be running on `http://127.0.0.1:5000`.

## Caching

The web application (aka the backend for the frontend aka SvelteKit server) caches the web service requests aggressively.
It will use up to **1GB of memory** for caching api requests made directly by browser
and **another 1Gb of memory** for caching api requests made by the backend for the frontend.

If you changed the data then the web service and the web application server must be restarted.
