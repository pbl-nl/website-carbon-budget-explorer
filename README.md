# Carbon Budget Explorer (CABE)

[![CI](https://github.com/carbon-budget-explorer/cabe/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/carbon-budget-explorer/cabe/actions/workflows/ci.yml)

Web application to explore carbon budgets

The web application is written with [SveltKit](https://kit.svelte.dev/).

## Data requirements

Should have the following data files:

1. `data/xr_dataread.nc` - NetCDF file
1. `data/xr_policyscen.nc` - NetCDF file
1. `data/xr_allow_<3 letter ISO countr code>.nc` - NetCDF file for each country
1. `data/xr_allow_<2030|2040|FC>.nc` - NetCDF file
1. `data/ne_110m_admin_0_countries.geojson` - can be downloaded with `npm run download:borders`

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

## Developing

You'll need [node.js](https://nodejs.org/en) to run a local development server.
Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

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

## Building

To create a production version of your app:

```bash
npm run build
```

You can the production build with

```bash
node build/index.js
```

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

If the Python webservice is not running on `http://127.0.0.1:5000` then set `CABE_API_URL` environment variable to right URL.
