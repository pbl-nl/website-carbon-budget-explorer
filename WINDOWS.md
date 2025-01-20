# Windows development setup

Tested on PDL werkomgeving.

## Install Git 

Not needed already installed.

## Clone repository

1. Open a command prompt.
2. Change the current working directory to the location where you want the cloned directory. For example `cd C:\Users\username\Documents`.
3. Run `git clone https://github.com/pbl-nl/website-carbon-budget-explorer.git`

Or use [Visual Studio Code](https://code.visualstudio.com/) to clone repository..

## Install software

Using miniforge to setup Python and Node.js.

1. From https://conda-forge..org/download download the latest Miniforge3 Windows 64-bit installer.
2. Create environment with `conda create --name cabe python=3.13 nodejs `
3. Activate environment with `conda activate cabe`
4. Install Python dependencies with `pip install -r requirements.txt waitress`
5. Install Node.js dependencies with `npm install`

Not allowed at step 1.

## Prepare data

Move the *.nc and *.geojson files to the `data` directory next to this file.

## Run Python web service

In the command prompt, run the following command:

```shell
# cd to the directory where you cloned the repository
waitress-serve --listen=127.0.0.1:5000 ws:app
```

## Run web application

In another command prompt, run the following command:

```shell
# cd to the directory where you cloned the repository
npm run dev
```

Visit http://localhost:5173 in your browser.
