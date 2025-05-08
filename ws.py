"""

Install with

    pip install flask gunicorn

Run with

    gunicorn -w 4 'ws:app'

"""

from dataclasses import dataclass
from json import loads
from pathlib import Path

import numpy as np
import pandas as pd
import sentry_sdk
import xarray as xr
from dotenv import dotenv_values
from effortsharing.allocation import allocation
from flask import Flask, jsonify, request
from flask_cors import CORS


@dataclass(frozen=True)
class Config:
    data_dir: Path
    start_year: str
    assumption_set: str


def load_env() -> Config:
    config = dotenv_values(".env")
    if "CABE_DATA_DIR" not in config or config["CABE_DATA_DIR"] is None:
        raise ValueError("CABE_DATA_DIR not set in .env file")
    if "CABE_START_YEAR" not in config or config["CABE_START_YEAR"] is None:
        raise ValueError("CABE_START_YEAR not set in .env file")
    if "CABE_ASSUMPTIONSET" not in config or config["CABE_ASSUMPTIONSET"] is None:
        raise ValueError("CABE_ASSUMPTIONSET not set in .env file")
    return Config(
        data_dir=Path(config["CABE_DATA_DIR"]),
        start_year=config["CABE_START_YEAR"],
        assumption_set=config["CABE_ASSUMPTIONSET"],
    )


config = load_env()

sentry_sdk.init(
    dsn="https://12eb01a8df644a3596e747a145f14033@app.glitchtip.com/10011",
    traces_sample_rate=0.0,
    profiles_sample_rate=0.0,
)

app = Flask(__name__)
CORS(app)

# TODO use class-based views for a reusable nc-file viewer?
# TODO write tests with dummy data

# Global data (xr_dataread.nc)
ds_global = xr.open_dataset(config.data_dir / config.start_year / "xr_dataread.nc")

# PCC convergence year is standard on 2050
DEFAULT_CONVERGENCE_YEAR = 2050

# ECPC discount factor
DEFAULT_DISCOUNT_FACTOR = 0.0

# Default start year for ECPC and GDR
DEFAULT_HISTORICAL_STARTYEAR = 1990

# GDR RCI weight
DEFAULT_RCI_WEIGHT = "Half"

# GDR capability threshold
DEFAULT_CAPABILITY_THRESHOLD = "Th"


@app.get("/timeseries/global/emissions/pathway")
def global_emission_pathway():
    """Get global carbon pathway for a given selection.

    To test:
    production server:
    http://127.0.0.1:8000/timeseries/global/emissions/pathway?exceedanceRisk=0.5&negativeEmissions=0.5

    dev server:
    http://127.0.0.1:5000/timeseries/global/emissions/pathway?exceedanceRisk=0.5&negativeEmissions=0.5
    """
    df = (
        (
            ds_global.GHG_globe.sel(
                # TODO remove defaults
                **global_pathway_choices(),
                Time=slice(2021, 2100),
            )
            / 1000  # global GHG in Gt CO2e
        )
        .rename({"Time": "time"})
        .to_pandas()
        .rename("value")
        .reset_index()
    )
    return df.to_dict(orient="records")


@app.get("/options/pathway/global")
def global_pathway_options():
    return {
        "temperature": ds_global.Temperature.values.tolist(),
        "exceedanceRisk": ds_global.Risk.values.tolist(),
        "nonCO2red": ds_global.NonCO2red.values.tolist(),
        "negativeEmissions": ds_global.NegEmis.values.tolist(),
        "timing": ds_global.Timing.values.tolist(),
    }


@app.get("/defaults/pathway/global")
def global_pathway_defaults():
    return {
        "temperature": 2.0,
        "exceedanceRisk": 0.5,
        "nonCO2red": 0.5,
        "negativeEmissions": 0.67,
        "timing": "Delayed",
    }


def global_pathway_choices():
    defaults = global_pathway_defaults()

    return dict(
        Temperature=request.args.get("temperature", defaults["temperature"]),
        Risk=request.args.get("exceedanceRisk", defaults["exceedanceRisk"]),
        NonCO2red=request.args.get("nonCO2red", defaults["nonCO2red"]),
        NegEmis=request.args.get("negativeEmissions", defaults["negativeEmissions"]),
        Timing=request.args.get("timing", defaults["timing"]),
    )


def find_region_files():
    region_dir = config.data_dir / config.start_year / config.assumption_set / "Allocations"
    available_region_files = {}
    for f in region_dir.glob("xr_alloc_*.nc"):
        region = f.stem.removeprefix("xr_alloc_")
        available_region_files[region] = f
    return available_region_files


available_region_files = find_region_files()


def read_geojson(fn: Path):
    """Remove all properties except NAME, ISO_A2_EH and ISO_A3_EH"""
    geojson = loads(fn.read_text(encoding="utf8"))
    for feature in geojson["features"]:
        feature["properties"] = {
            "NAME": feature["properties"]["NAME"],
            "ISO_A2_EH": feature["properties"]["ISO_A2_EH"],
            "ISO_A3_EH": feature["properties"]["ISO_A3_EH"],
        }
    return geojson


country_border_geojson_file = config.data_dir / "ne_110m_admin_0_countries.geojson"
country_border_geojson = read_geojson(country_border_geojson_file)


@app.get("/borders")
def borders():
    """/borders should return

    ```geojson
    {
    type: 'FeatureCollection',
    name: 'ne_110m_admin_0_countries',
    crs: {
        type: 'name',
        properties: { name: 'urn:ogc:def:crs:OGC:1.3:CRS84' }
    },
    features: [
        {
    type: 'Feature',
    properties: { ISO_A3_EH: 'FJI', NAME: 'Fiji' },
    bbox: [ -180, -18.28799, 180, -16.020882 ],
    geometry: { type: 'MultiPolygon', coordinates: [ [Array], [Array], [Array] ] }
    }],
    bbox: [ -180, -90, 180, 83.64513 ]
    }
    ```
    """
    return country_border_geojson


def build_regions():
    countries_from_geojson = {}
    for g in country_border_geojson["features"]:
        ps = g["properties"]
        countries_from_geojson[ps["ISO_A3_EH"]] = {
            "name": ps["NAME"],
            "iso2": ps["ISO_A2_EH"],
            "iso3": ps["ISO_A3_EH"],
        }

    # TODO store this in nc file
    additional_regions = {
        "MLT": {"iso2": "MT", "iso3": "MLT", "name": "Malta"},
        "STP": {"iso2": "ST", "iso3": "STP", "name": "São Tomé and Príncipe"},
        "MUS": {"iso2": "MU", "iso3": "MUS", "name": "Mauritius"},
        "PLW": {"iso2": "PW", "iso3": "PLW", "name": "Palau"},
        "ATG": {"iso2": "AG", "iso3": "ATG", "name": "Antigua and Barbuda"},
        "BRB": {"iso2": "BB", "iso3": "BRB", "name": "Barbados"},
        "Northern America": {
            "iso2": None,
            "iso3": "Northern America",
            "name": "Northern America",
        },
        "VCT": {
            "iso2": "VC",
            "iso3": "VCT",
            "name": "Saint Vincent and the Grenadines",
        },
        "EU": {"iso2": "EU", "iso3": "EU", "name": "European Union"},
        "CPV": {"iso2": "CV", "iso3": "CPV", "name": "Cape Verde"},
        "BHR": {"iso2": "BH", "iso3": "BHR", "name": "Bahrain"},
        "SIDS": {
            "iso3": "SIDS",
            "name": "Small Island Developing States",
        },
        "KNA": {"iso2": "KN", "iso3": "KNA", "name": "Saint Kitts and Nevis"},
        "MCO": {"iso2": "MC", "iso3": "MCO", "name": "Monaco"},
        "TON": {"iso2": "TO", "iso3": "TON", "name": "Tonga"},
        "Umbrella": {"iso2": None, "iso3": "Umbrella", "name": "Umbrella"},
        "COM": {"iso2": "KM", "iso3": "COM", "name": "Comoros"},
        "KIR": {"iso2": "KI", "iso3": "KIR", "name": "Kiribati"},
        "GRD": {"iso2": "GD", "iso3": "GRD", "name": "Grenada"},
        "EARTH": {"iso2": None, "iso3": "EARTH", "name": "Earth"},
        "SYC": {"iso2": "SC", "iso3": "SYC", "name": "Seychelles"},
        "NRU": {"iso2": "NR", "iso3": "NRU", "name": "Nauru"},
        "WSM": {"iso2": "WS", "iso3": "WSM", "name": "Samoa"},
        "AND": {"iso2": "AD", "iso3": "AND", "name": "Andorra"},
        "Australasia": {
            "iso2": None,
            "iso3": "Australasia",
            "name": "Australasia",
        },
        "DMA": {"iso2": "DM", "iso3": "DMA", "name": "Dominica"},
        "SGP": {"iso2": "SG", "iso3": "SGP", "name": "Singapore"},
        "TUV": {"iso2": "TV", "iso3": "TUV", "name": "Tuvalu"},
        "LIE": {"iso2": "LI", "iso3": "LIE", "name": "Liechtenstein"},
        "SMR": {"iso2": "SM", "iso3": "SMR", "name": "San Marino"},
        "LCA": {"iso2": "LC", "iso3": "LCA", "name": "Saint Lucia"},
        "MHL": {"iso2": "MH", "iso3": "MHL", "name": "Marshall Islands"},
        "G7": {"iso2": None, "iso3": "G7", "name": "Group of Seven (G7)"},
        "VAT": {"iso2": "VA", "iso3": "VAT", "name": "Vatican City"},
        "African Group": {
            "iso2": None,
            "iso3": "African Group",
            "name": "African Group",
        },
        "FSM": {"iso2": "FM", "iso3": "FSM", "name": "Micronesia"},
        "G20": {"iso2": None, "iso3": "G20", "name": "Group of 20 (G20)"},
        "LDC": {
            "iso2": None,
            "iso3": "LDC",
            "name": "Least developed countries",
        },
        "NIU": {"iso2": "NU", "iso3": "NIU", "name": "Niue"},
        "COK": {"iso2": "CK", "iso3": "COK", "name": "Cook Islands"},
        "MDV": {"iso2": "MV", "iso3": "MDV", "name": "Maldives"},
    }

    global_regions = set(ds_global.Region.values.tolist())
    data = []
    for region in global_regions:
        if region in available_region_files and region in global_regions:
            if region in countries_from_geojson:
                data.append(countries_from_geojson[region])
            else:
                data.append(additional_regions[region])

    countries_of_regions = {
        "EU": [
            "AUT",
            "BEL",
            "BGR",
            "CYP",
            "CZE",
            "DEU",
            "DNK",
            "ESP",
            "EST",
            "FIN",
            "FRA",
            "GRC",
            "HRV",
            "HUN",
            "IRL",
            "ITA",
            "LTU",
            "LUX",
            "LVA",
            "MLT",
            "NLD",
            "POL",
            "PRT",
            "ROU",
            "SVK",
            "SVN",
            "SWE",
        ],
        "African Group": [
            "AGO",
            "BDI",
            "BEN",
            "BFA",
            "BWA",
            "CAF",
            "CIV",
            "CMR",
            "COD",
            "COG",
            "COM",
            "CPV",
            "DJI",
            "DZA",
            "EGY",
            "ERI",
            "ETH",
            "GAB",
            "GHA",
            "GIN",
            "GMB",
            "GNB",
            "GNQ",
            "KEN",
            "LBR",
            "LBY",
            "LSO",
            "MAR",
            "MDG",
            "MLI",
            "MOZ",
            "MRT",
            "MUS",
            "MWI",
            "NAM",
            "NER",
            "NGA",
            "RWA",
            "SDN",
            "SEN",
            "SLE",
            "SOM",
            "SSD",
            "STP",
            "SWZ",
            "SYC",
            "TCD",
            "TGO",
            "TUN",
            "TZA",
            "UGA",
            "ZAF",
            "ZMB",
            "ZWE",
        ],
        "Northern America": ["CAN", "USA"],
        "Australasia": ["AUS", "NZL"],
        "Umbrella": ["AUS", "CAN", "ISL", "ISR", "JPN", "KAZ", "NOR", "NZL", "UKR", "USA"],
        "G7": ["CAN", "DEU", "FRA", "GBR", "ITA", "JPN", "USA"],
        "G20": [
            "ARG",
            "AUS",
            "AUT",
            "BEL",
            "BGR",
            "BRA",
            "CAN",
            "CHN",
            "CYP",
            "CZE",
            "DEU",
            "DNK",
            "ESP",
            "EST",
            "FIN",
            "FRA",
            "GBR",
            "GRC",
            "HRV",
            "HUN",
            "IDN",
            "IND",
            "IRL",
            "ITA",
            "JPN",
            "KOR",
            "LTU",
            "LUX",
            "LVA",
            "MEX",
            "MLT",
            "NLD",
            "POL",
            "PRT",
            "ROU",
            "RUS",
            "SAU",
            "SVK",
            "SVN",
            "SWE",
            "TUR",
            "USA",
            "ZAF",
        ],
        "FSM": ["MHL"],
        "LDC": [
            "AFG",
            "AGO",
            "BDI",
            "BEN",
            "BFA",
            "BGD",
            "BTN",
            "CAF",
            "COD",
            "COM",
            "DJI",
            "ERI",
            "ETH",
            "GIN",
            "GMB",
            "GNB",
            "HTI",
            "KHM",
            "KIR",
            "LAO",
            "LBR",
            "LSO",
            "MDG",
            "MLI",
            "MMR",
            "MOZ",
            "MRT",
            "MWI",
            "NER",
            "NPL",
            "RWA",
            "SDN",
            "SEN",
            "SLB",
            "SLE",
            "SOM",
            "SSD",
            "STP",
            "TCD",
            "TGO",
            "TLS",
            "TUV",
            "TZA",
            "UGA",
            "YEM",
            "ZMB",
        ],
        "SIDS": [
            "ATG",
            "BHS",
            "BLZ",
            "BRB",
            "COK",
            "COM",
            "CPV",
            "CUB",
            "DMA",
            "DOM",
            "FJI",
            "FSM",
            "GNB",
            "GRD",
            "GUY",
            "HTI",
            "JAM",
            "KIR",
            "KNA",
            "LCA",
            "MDV",
            "MHL",
            "MUS",
            "NIU",
            "NRU",
            "PLW",
            "PNG",
            "SGP",
            "SLB",
            "STP",
            "SUR",
            "SYC",
            "TLS",
            "TON",
            "TTO",
            "TUV",
            "VCT",
            "VUT",
            "WSM",
        ],
    }
    for region in data:
        if region["iso3"] in countries_of_regions:
            region["countries"] = countries_of_regions[region["iso3"]]
        for region2, countries in countries_of_regions.items():
            if region["iso3"] in countries:
                if "regions" not in region:
                    region["regions"] = []
                region["regions"] = sorted(region["regions"] + [region2])

    return sorted(data, key=lambda x: x["name"])


available_regions = build_regions()


@app.get("/regions")
def regions():
    return available_regions


@app.get("/regions/<region>")
def region(region):
    for r in available_regions:
        if r["iso3"] == region:
            return r
    raise ValueError(f"Region {region} not found")


@app.get("/statistics/budget/global")
def budget():
    hist = ds_global.CO2_hist
    remaining = ds_global.sel(**global_pathway_choices()).Budget.values.tolist()
    reference = hist.sel(Region="EARTH").sel(Time=2021).item()
    relative = remaining / reference
    return {"remaining": remaining, "relative": relative * 1000}


@app.get("/statistics/gap/global")
def gap():
    globe = ds_global.GHG_globe
    gap_index = 2030
    pathway = globe.sel(Time=gap_index, **global_pathway_choices()).values + 0
    # TODO do not calculate mean here, but precalculate it
    cur_pol = ds_policyscen.CurPol.sel(Region="EARTH", Time=gap_index).mean().values + 0
    ndc = ds_policyscen.NDC.sel(Region="EARTH", Time=gap_index).mean().values + 0
    return {
        "index": gap_index,
        "budget": pathway / 1000,
        "curPol": cur_pol / 1000,
        "ndc": ndc / 1000,
    }


@app.get("/timeseries/<region>/emissions/historical")
def historical_emissions(region="EARTH"):
    start = request.args.get("start")
    end = request.args.get("end")
    df = ds_global.GHG_hist.sel(Region=region, Time=slice(start, end)).to_pandas()

    if region == "EARTH":
        df /= 1000  # global GHG in Gt CO2e

    df = df.reset_index().rename(columns={"Time": "time", "GHG_hist": "value"}).dropna()
    return df.to_dict(orient="records")


def population_map(year, scenario="SSP2"):
    """Return population map as xarray data-array"""
    return ds_global.Population.sel(Time=year, Scenario=scenario)


def open_aggregated_files():
    root = config.data_dir / config.start_year / config.assumption_set / "Aggregated_files"
    files = {}
    for f in root.glob("xr_alloc_*.nc"):
        # TODO once https://github.com/pbl-nl/website-carbon-budget-explorer/issues/38#issuecomment-2653487809
        # the removesuffix is no longer needed
        year = f.stem.removeprefix("xr_alloc_")
        files[year] = xr.open_dataset(f)
    return files


file_by_year = open_aggregated_files()


@app.get("/map/<year>/<allocation_method>")
def allocation_map(year, allocation_method):
    """Get map of GHG by year"""
    selection = global_pathway_choices()
    if allocation_method in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        selection.update(Scenario="SSP2")
    if allocation_method in ["PCC", "ECPC"]:
        selection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
    if allocation_method in ["ECPC", "GDR"]:
        selection.update(Historical_startyear=DEFAULT_HISTORICAL_STARTYEAR)
    if allocation_method == "ECPC":
        selection.update(Discount_factor=DEFAULT_DISCOUNT_FACTOR)
    if allocation_method == "GDR":
        selection.update(RCI_weight=DEFAULT_RCI_WEIGHT, Capability_threshold=DEFAULT_CAPABILITY_THRESHOLD)

    df = (
        (
            file_by_year[year][allocation_method].sel(**selection)
            # TODO: precalculate per capita data instead of division below?
            / population_map(year=2021)
        )
        .to_series()
        .rename("value")
        .dropna()  # Note: dropping NaN values here
        .reset_index()
    )
    rows = df.to_dict(orient="records")

    ds = (
        file_by_year[year].sel(
            Scenario="SSP2",
            Convergence_year=DEFAULT_CONVERGENCE_YEAR,
            **global_pathway_choices(),
        )
    ).to_array("variable")

    domain = [ds.quantile(0.2).item(), ds.quantile(0.44).item()]

    # Round domain to nearest 3
    domain = [d // 3 * 3 for d in domain]
    return {"data": rows, "domain": domain}


# Reference pathway data (xr_policyscen.nc)
ds_policyscen = xr.open_dataset(config.data_dir / "xr_policyscen.nc")


@app.get("/timeseries/<region>/policies/<policy>")
def policy(policy, region):
    assert policy in {"CurPol", "NDC", "NetZero"}
    policy_ds = ds_policyscen[policy].sel(Region=region, Time=slice(2021, 2100)).drop("Region")
    # Not all countries have data for all policies, so return None if no data
    if policy_ds.isnull().all():
        return jsonify(None)

    policy_ds = policy_ds.groupby("Time")

    # TODO precompute mean, min and max
    # instead of calculating them on the fly each time
    df = xr.merge(
        [
            policy_ds.mean(["Model"]).rename("mean"),
            policy_ds.min(["Model"]).rename("min"),
            policy_ds.max(["Model"]).rename("max"),
        ]
    ).to_pandas()

    if region == "EARTH":
        columns_to_divide = ["mean", "min", "max"]
        df[columns_to_divide] = df[columns_to_divide] / 1000  # global GHG in Gt CO2e

    df.index.rename("time", inplace=True)
    return df.reset_index().to_dict(orient="records")


def is_eu(region):
    # EU member states do not have individual NDCs but are covered by the EU NDC
    member_states = {
        "AUT",
        "BEL",
        "BGR",
        "HRV",
        "CYP",
        "CZE",
        "DNK",
        "EST",
        "FIN",
        "FRA",
        "DEU",
        "GRC",
        "HUN",
        "IRL",
        "ITA",
        "LVA",
        "LTU",
        "LUX",
        "MLT",
        "NLD",
        "POL",
        "PRT",
        "ROU",
        "SVK",
        "SVN",
        "ESP",
        "SWE",
    }
    if region in member_states:
        return "EU"
    return region


@app.get("/statistics/ndc/reductions/<region>")
def ndc_reductions(region):
    region = is_eu(region)

    ndc2030_min = ds_global.GHG_ndc_red.sel(Region=region).min().values.tolist()
    ndc2030_max = ds_global.GHG_ndc_red.sel(Region=region).max().values.tolist()

    if np.isnan(ndc2030_min) or np.isnan(ndc2030_max):
        return jsonify(None)
    return {"min": ndc2030_min * 100, "max": ndc2030_max * 100}

    # ndc2030_min = dsGlobal.GHG_ndc.sel(Region=region).min().values.tolist()
    # ndc2030_max = dsGlobal.GHG_ndc.sel(Region=region).max().values.tolist()

    # hist2015 = dsGlobal.GHG_hist.sel(Region=region, Time=2015).values.tolist()
    # return {
    #     "min": -(ndc2030_max - hist2015) / hist2015 * 100,
    #     "max": -(ndc2030_min - hist2015) / hist2015 * 100
    # }


def ndc_range_inventory(region):
    # Absolute emissions from the NDC, based on self-reported inventory data
    region = is_eu(region)

    ds_ndc_inv = ds_global.GHG_ndc_inv.sel(Region=region)
    min_ndc_inv = ds_ndc_inv.min().values.tolist()
    max_ndc_inv = ds_ndc_inv.max().values.tolist()
    if np.isnan(min_ndc_inv) or np.isnan(max_ndc_inv):
        return None
    return {2030: [min_ndc_inv, max_ndc_inv]}


def ndc_range_jones(region):
    # Is using GHGH_ndc_red to get absolute emissions, but then using 2015 Jones data
    region = is_eu(region)

    ds_ndc = ds_global.GHG_ndc.sel(Region=region)
    ds_ndc_min = ds_ndc.min().values.tolist()
    ds_ndc_max = ds_ndc.max().values.tolist()
    if np.isnan(ds_ndc_min) or np.isnan(ds_ndc_max):
        return None
    return {2030: [ds_ndc_min, ds_ndc_max]}


@app.get("/statistics/ndc/projections/<region>")
def ndc_projections(region):
    return {"ndc_inventory": ndc_range_inventory(region), "ndc_jones": ndc_range_jones(region)}


def get_ds(region):
    if region not in available_region_files:
        raise ValueError(f"Region {region} not found")
    fn = available_region_files[region]
    return xr.open_dataset(fn)


def emission_allocation_per_method_old(region, allocation_method):
    selection = global_pathway_choices()
    ds = get_ds(region)[allocation_method].sel(**selection).rename(Time="time")
    # set time as the first dimension
    dim_order = ["time"] + [dim for dim in ds.dims if dim != "time"]
    ds = ds.transpose(*dim_order)

    # extract the 'most reasonable' (mr) df which will be the main trajectory line
    mr_selection = dict()
    if allocation_method in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        mr_selection.update(Scenario="SSP2")
    if allocation_method in ["PCC", "ECPC"]:
        mr_selection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
    if allocation_method in ["ECPC", "GDR"]:
        mr_selection.update(Historical_startyear=DEFAULT_HISTORICAL_STARTYEAR)
    if allocation_method == "ECPC":
        mr_selection.update(
            Discount_factor=DEFAULT_DISCOUNT_FACTOR,
        )
    if allocation_method == "GDR":
        mr_selection.update(RCI_weight=DEFAULT_RCI_WEIGHT, Capability_threshold=DEFAULT_CAPABILITY_THRESHOLD)

    mr_df = ds.sel(**mr_selection).to_pandas().rename("mean")

    if mr_df.isna().all():
        return None

    agg_dims = [dim for dim in ds.dims if dim != "time"]
    min_df = ds.min(agg_dims, skipna=True).to_pandas().rename("min")
    max_df = ds.max(agg_dims, skipna=True).to_pandas().rename("max")

    return pd.concat([mr_df, min_df, max_df], axis=1).reset_index().dropna().to_dict(orient="records")


allocation_methods = {"PC", "PCC", "AP", "GDR", "ECPC", "GF"}

def emission_allocation_per_method(allocator_ds, allocation_method):
    ds = allocator_ds.rename(Time="time")
    dim_order = ["time"] + [dim for dim in ds.dims if dim != "time"]
    ds = ds.transpose(*dim_order)

    # extract the 'most reasonable' (mr) df which will be the main trajectory line
    mr_selection = dict()
    if allocation_method in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        mr_selection.update(Scenario="SSP2")
    if allocation_method in ["PCC", "ECPC"]:
        mr_selection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
    if allocation_method in ["ECPC", "GDR"]:
        mr_selection.update(Historical_startyear=DEFAULT_HISTORICAL_STARTYEAR)
    if allocation_method == "ECPC":
        mr_selection.update(
            Discount_factor=DEFAULT_DISCOUNT_FACTOR,
        )
    if allocation_method == "GDR":
        mr_selection.update(RCI_weight=DEFAULT_RCI_WEIGHT, Capability_threshold=DEFAULT_CAPABILITY_THRESHOLD)

    mr_df = ds.sel(**mr_selection).to_pandas().rename("mean")

    if mr_df.isna().all():
        return None

    agg_dims = [dim for dim in ds.dims if dim != "time"]
    min_df = ds.min(agg_dims, skipna=True).to_pandas().rename("min")
    max_df = ds.max(agg_dims, skipna=True).to_pandas().rename("max")

    return pd.concat([mr_df, min_df, max_df], axis=1).reset_index().dropna().to_dict(orient="records")

@app.get("/timeseries/<region>/emissions/allocations")
def emission_allocations(region):
    allocator = create_allocator(region)
    allocations = {}
    selection = global_pathway_choices()
    for allocation_method in allocation_methods:
        allocation_data = emission_allocation_per_method(
            allocator.xr_total[allocation_method].sel(**selection), 
            allocation_method,
        )
        if allocation_data is None:
            continue
        allocations[allocation_method] = allocation_data
    return allocations


def create_allocator(region):
    lulucf="incl"
    gas="GHG"
    input_file = '../effort-sharing/notebooks/input.yml'
    allocator = allocation(
        region, lulucf=lulucf, gas=gas,
        input_file=input_file,
    )
    allocator.gf()
    allocator.pc()
    allocator.pcc()
    allocator.pcb()
    allocator.dim_convyears = [DEFAULT_CONVERGENCE_YEAR]
    allocator.ecpc()
    allocator.ap()
    allocator.gdr()
    return allocator

def emission_allocations_old(region):
    """
    http://127.0.0.1:5000/timeseries/USA/emissions/allocations?exceedanceRisk=0.67&negativeEmissions=0.4&temperature=1.8: 36.94ms
    """
    allocations = {}
    for allocation_method in allocation_methods:
        allocation = emission_allocation_per_method_old(region, allocation_method)
        if allocation is None:
            continue
        allocations[allocation_method] = allocation
    return allocations


@app.get("/statistics/reductions/<region>")
def allocation_reduction(region):
    periods = (2030, 2040)
    selection = dict(
        **global_pathway_choices(),
        Time=periods,
    )

    hist = ds_global.GHG_hist.sel(Region=region, Time=1990).values + 0

    allocator = create_allocator(region)
    reductions = {}
    for allocation_method in allocation_methods:
        pselection = selection.copy()
        if allocation_method in ["PC", "PCC", "AP", "GDR", "ECPC"]:
            pselection.update(Scenario="SSP2")
        if allocation_method in ["PCC", "ECPC"]:
            pselection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
        reductions[allocation_method] = {}
        for period in periods:
            pselection.update(Time=period)
            es = allocator.xr_total[allocation_method].sel(**pselection).mean().values + 0
            if np.isnan(es) or np.isnan(hist) or hist == 0:
                reductions[allocation_method][period] = None
            else:
                reductions[allocation_method][period] = -(es - hist) / hist * 100

    return reductions

def allocation_reduction_old(region):
    periods = (2030, 2040)
    selection = dict(
        **global_pathway_choices(),
        Time=periods,
    )

    hist = ds_global.GHG_hist.sel(Region=region, Time=1990).values + 0
    ds = get_ds(region)

    reductions = {}
    for allocation_method in allocation_methods:
        pselection = selection.copy()
        if allocation_method in ["PC", "PCC", "AP", "GDR", "ECPC"]:
            pselection.update(Scenario="SSP2")
        if allocation_method in ["PCC", "ECPC"]:
            pselection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
        reductions[allocation_method] = {}
        for period in periods:
            pselection.update(Time=period)
            es = ds[allocation_method].sel(**pselection).mean().values + 0
            if np.isnan(es) or np.isnan(hist) or hist == 0:
                reductions[allocation_method][period] = None
            else:
                reductions[allocation_method][period] = -(es - hist) / hist * 100

    return reductions


if __name__ == "__main__":
    print(create_allocator("BRA"))
