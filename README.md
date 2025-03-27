# Carbon Budget Explorer (CABE)

[![CI](https://github.com/carbon-budget-explorer/cabe/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/carbon-budget-explorer/cabe/actions/workflows/ci.yml)

Web application to explore carbon budgets

The web application is written with [SveltKit](https://kit.svelte.dev/).

## Data requirements and configuration

Should have the following data files:

1. `{CABE_DATA_DIR} / "ne_110m_admin_0_countries.geojson"` - can be downloaded with `npm run download:borders` and move downloaded file to CABE_DATA_DIR directory.
1. `{CABE_DATA_DIR} / "xr_policyscen.nc"`- Policy scenario data
1. `{CABE_DATA_DIR} / {CABE_START_YEAR} / "xr_dataread.nc"` - Global data
1. `{CABE_DATA_DIR} / {CABE_START_YEAR} / {CABE_ASSUMPTIONSET} / "Allocations" / "xr_alloc_{REGION}.nc"` - Region specific data
1. `{CABE_DATA_DIR} / {CABE_START_YEAR} / {CABE_ASSUMPTIONSET} / "Aggregated_files" / "xr_alloc_{YEAR}.nc"` - Aggregated data

The `CABE_DATA_DIR` variable is the path to the data directory.
The `CABE_START_YEAR` variable is the start year of the allocation.
The `CABE_ASSUMPTIONSET` variable encodes assumptions on which gases are included (GHG or CO2_only) and land use (included/excluded).
The `REGION` variable is the 3 letter ISO code of the region.
The `YEAR` variable is the year of the allocation.

The `CABE_` variables are defined in the `.env` file.
See [.env.example](.env.example) file for an example.
To run the application the `.env` file is required.

## Software requirements

You should have [Node.js](https://nodejs.org/en) (v22 or greater) and Python 3.12 installed.

Dependencies can be installed with

```bash
# From the root of the repository
# To install Node.js dependencies
npm install
# To install Python dependencies
pip install -r requirements.txt
```

## Software installation on Windows

Use miniforge to setup Python and Node.js.

1. From [https://conda-forge.org/download](https://conda-forge.org/download/) download the latest Miniforge3 Windows 64-bit installer and install it.
2. Open a PowerShell
3. Create environment with `mamba create --name cabe python=3.12 nodejs=22`
4. Activate environment with `mamba activate cabe`
5. Change the current working directory to the location where you want to clone the repository. For example `cd C:\Users\username\Documents`.
6. Clone repo with `git clone https://github.com/pbl-nl/website-carbon-budget-explorer.git` or use [Visual Studio Code](https://code.visualstudio.com/) to clone repository.
7. Change the current working directory to the repository with `cd website-carbon-budget-explorer`.
8. Install Python dependencies with `pip install -r requirements.txt`
9. Install Node.js dependencies with `npm install`

If `git` executable is not installed, then install with `mamba install git`.

If `mamba` executable is not available, use `conda` instead.

Do not forget to activate the environment with `mamba activate cabe` before running the commands below.

## API service

The API web service reads the NetCDF files and returns the data as JSON which is used in the web application.

It is written in Python using [Flask](https://flask.palletsprojects.com/) and [xarray](https://xarray.dev/).

On Linux and MacOS the web service can be started with

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 'ws:app'
```

(Add `--reload` argumment to reload on Python file changes)

On Windows, use flask built-in developer server.

```shell
flask --app ws:app run -p 5000
```

If an error occurs here, try out different ports (e.g. 5001, 5005 etc). Also adjust the changed port in the `.env` file.
To see the routes of the web service use

```bash
flask --app ws:app routes -s rule
```

## Developing

Start a development server:

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

The Python web service (ws.py) can be formatted and linted with [Ruff](https://docs.astral.sh/ruff)

```bash
pip install ruff
ruff check
ruff format
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
