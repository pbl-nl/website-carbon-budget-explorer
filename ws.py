"""

Install with

    pip install flask gunicorn

Run with

    gunicorn -w 4 'ws:app'

"""
from dataclasses import dataclass
from json import loads
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import xarray as xr
import pandas as pd
import sentry_sdk
from dotenv import dotenv_values

@dataclass(frozen=True)
class Config:
    data_dir: Path
    start_year: str
    assumption_set: str

def load_env() -> Config:
    config = dotenv_values(".env")
    if 'CABE_DATA_DIR' not in config or config['CABE_DATA_DIR'] is None:
        raise ValueError("CABE_DATA_DIR not set in .env file")
    if 'CABE_START_YEAR' not in config or config['CABE_START_YEAR'] is None:
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

# TODO improve endpoint names
# TODO use class-based views for a reusable nc-file viewer?
# TODO write tests with dummy data

# Global data (xr_dataread.nc)
dsGlobal = xr.open_dataset(config.data_dir / config.start_year / "xr_dataread.nc")

# PCC convergence year is standard on 2050
DEFAULT_CONVERGENCE_YEAR = 2050

# ECPC discount factor
DEFAULT_DISCOUNT_FACTOR = 0.0

# Default start year for ECPC and GDR
DEFAULT_HISTORICAL_STARTYEAR = 1990

# GDR RCI weight
DEFAULT_RCI_WEIGHT = 'Half'

# GDR capability threshold
DEFAULT_CAPABILITY_THRESHOLD = 'Th'


@app.get("/timeseries/global/emissions/pathway")
def globalPathway():
    """Get global carbon pathway for a given selection.

    To test:
    production server:
    http://127.0.0.1:8000/pathwayCarbon?exceedanceRisk=0.5&negativeEmissions=0.5

    dev server:
    http://127.0.0.1:5000/pathwayCarbon?exceedanceRisk=0.5&negativeEmissions=0.5
    """
    df = (
        (
            dsGlobal.GHG_globe.sel(
                # TODO remove defaults
                # TODO use request.data instead of request.args?
                # args uses GET, data uses POST, GET is idempotent which is easier to cache so keep using args
                **globalPathwayChoices(),
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
def globalPathwayOptions():
    return {
        "temperature": dsGlobal.Temperature.values.tolist(),
        "exceedanceRisk": dsGlobal.Risk.values.tolist(),
        "negativeEmissions": dsGlobal.NegEmis.values.tolist(),
        "timing": dsGlobal.Timing.values.tolist(),
        "nonCO2red": dsGlobal.NonCO2red.values.tolist()
    }


def globalPathwayChoices():
    # TODO fix slider settings
    # this specifies the defaults that are shown in the global graph, but not the default slider settings!
    defaults = {'temperature': 2.0,
                'exceedanceRisk': 0.5,
                'negativeEmissions': 0.5,
                'timing': 'Immediate',
                'nonCO2red': 0.5}

    return dict(
        Temperature=request.args.get("temperature", defaults["temperature"]),
        Risk=request.args.get("exceedanceRisk", defaults["exceedanceRisk"]),
        NegEmis=request.args.get("negativeEmissions", defaults["negativeEmissions"]),
        Timing=request.args.get("timing", defaults["timing"]),
        NonCO2red=request.args.get("nonCO2red", defaults["nonCO2red"])
    )


def find_region_files():
    region_dir = (
        config.data_dir / config.start_year / config.assumption_set / "Allocations"
    )
    available_region_files = {}
    for f in region_dir.glob("xr_alloc_*.nc"):
        iso = f.stem.removeprefix("xr_alloc_")
        available_region_files[iso] = f
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

    global_regions = set(dsGlobal.Region.values.tolist())
    data = []
    for region in global_regions:
        if region in available_region_files and region in global_regions:
            if region in countries_from_geojson:
                data.append(countries_from_geojson[region])
            else:
                data.append(additional_regions[region])
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
    hist = dsGlobal.CO2_hist
    remaining = dsGlobal.sel(**globalPathwayChoices()).Budget.values.tolist()
    reference = hist.sel(Region="EARTH").sel(Time=2021).item()
    relative = remaining / reference
    return {
        "remaining": remaining,
        "relative": relative * 1000
    }

@app.get("/statistics/gap/global")
def gap():
    globe = dsGlobal.GHG_globe
    gap_index = 2030
    pathway = (
        globe.sel(Time=gap_index, **globalPathwayChoices())
        .values
        + 0
    )
    # TODO do not calculate mean here, but precalculate it
    curPol = ds_policyscen.CurPol.sel(Region="EARTH", Time=gap_index).mean().values + 0
    ndc = ds_policyscen.NDC.sel(Region="EARTH", Time=gap_index).mean().values + 0
    return {
        "index": gap_index,
        "budget": pathway / 1000,
        "curPol": curPol / 1000,
        "ndc": ndc / 1000,
        "emission": (curPol - pathway) / 1000,
        "ambition": (ndc - pathway) / 1000,
    }


@app.get("/timeseries/<region>/emissions/historical")
def historicalEmissions(region="EARTH"):
    start = request.args.get("start")
    end = request.args.get("end")
    df = dsGlobal.GHG_hist.sel(Region=region, Time=slice(start, end)).to_pandas()

    if region == "EARTH":
        df /= 1000  # global GHG in Gt CO2e

    df = df.reset_index().rename(columns={'Time': 'time', 'GHG_hist': "value"}).dropna()
    return df.to_dict(orient="records")

def population_map(year, scenario="SSP2"):
    """Return population map as xarray data-array"""
    return dsGlobal.Population.sel(Time=year, Scenario=scenario)

def open_aggregated_files():
    root = (
        config.data_dir / config.start_year / config.assumption_set / "Aggregated_files"
    )
    files = {}
    for f in root.glob("xr_alloc_*.nc"):
        # TODO once https://github.com/pbl-nl/website-carbon-budget-explorer/issues/38#issuecomment-2653487809
        # the removesuffix is no longer needed
        year = f.stem.removeprefix("xr_alloc_")
        files[year] = xr.open_dataset(f)
    return files

file_by_year = open_aggregated_files()

@app.get("/map/<year>/<effortSharing>")
def fullCenturyBudgetSpatial(year, effortSharing):
    """Get map of GHG by year"""
    selection = globalPathwayChoices()
    if effortSharing in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        selection.update(Scenario="SSP2")
    if effortSharing == "PCC":
        selection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
    if effortSharing in ["ECPC", "GDR"]:
        selection.update(Historical_startyear=DEFAULT_HISTORICAL_STARTYEAR)
    if effortSharing == "ECPC":
        selection.update(Discount_factor=DEFAULT_DISCOUNT_FACTOR)
    if effortSharing == "GDR":
        selection.update(RCI_weight=DEFAULT_RCI_WEIGHT,
                         Capability_threshold=DEFAULT_CAPABILITY_THRESHOLD)

    df = (
        (
            file_by_year[year][effortSharing]
            .sel(**selection)
             # TODO: precalculate per capita data instead of division below?
            / population_map(year=2021)
        )
        .rename(Region="ISO")
        .to_series()
        .rename("value")
        .dropna()  # Note: dropping NaN values here
        .reset_index()
    )
    rows = df.to_dict(orient="records")

    ds = (
        file_by_year[year]
        .sel(
            Scenario="SSP2",
            Convergence_year=DEFAULT_CONVERGENCE_YEAR,
            **globalPathwayChoices(),
        )
    ).to_array("variable")

    domain = [ds.quantile(0.2).item(), ds.quantile(0.44).item()]

    # Round domain to nearest 3
    domain = [d // 3 * 3 for d in domain]
    return {"data": rows, "domain": domain}


# Reference pathway data (xr_policyscen.nc)
ds_policyscen = xr.open_dataset(config.data_dir / "xr_policyscen.nc")


@app.get("/timeseries/<region>/policies/<policy>")
def policyPathway(policy, region):
    assert policy in {"CurPol", "NDC", "NetZero"}
    policy_ds = (
        ds_policyscen[policy].sel(Region=region, Time=slice(2021, 2100)).drop("Region")
    )
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
        columns_to_divide = ['mean', 'min', 'max']
        df[columns_to_divide] = df[columns_to_divide] / 1000  # global GHG in Gt CO2e

    df.index.rename("time", inplace=True)
    return df.reset_index().to_dict(orient="records")


def isEU(region):
    # EU member states do not have individual NDCs but are covered by the EU NDC
    member_states = [
        "AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA",
        "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD",
        "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"
    ]
    if region in member_states:
        return "EU"
    return region


@app.get("/statistics/ndcReductions/<region>")
def ndcReductions(region):
    region = isEU(region)

    ndc2030_min = dsGlobal.GHG_ndc_red.sel(Region=region).min().values.tolist()
    ndc2030_max = dsGlobal.GHG_ndc_red.sel(Region=region).max().values.tolist()

    if np.isnan(ndc2030_min) or np.isnan(ndc2030_max):
        return None
    return {
        "min": ndc2030_min * 100,
        "max": ndc2030_max * 100
    }

    # ndc2030_min = dsGlobal.GHG_ndc.sel(Region=region).min().values.tolist()
    # ndc2030_max = dsGlobal.GHG_ndc.sel(Region=region).max().values.tolist()

    # hist2015 = dsGlobal.GHG_hist.sel(Region=region, Time=2015).values.tolist()
    # return {
    #     "min": -(ndc2030_max - hist2015) / hist2015 * 100,
    #     "max": -(ndc2030_min - hist2015) / hist2015 * 100
    # }


def ndcRange_inventory(region):
    # Absolute emissions from the NDC, based on self-reported inventory data
    region = isEU(region)

    ds_ndc_inv = dsGlobal.GHG_ndc_inv.sel(Region=region)
    min_ndc_inv = ds_ndc_inv.min().values.tolist()
    max_ndc_inv = ds_ndc_inv.max().values.tolist()
    if np.isnan(min_ndc_inv) or np.isnan(max_ndc_inv):
        return None
    return {2030: [min_ndc_inv, max_ndc_inv]}


def ndcRange_jones(region):
    # Is using GHGH_ndc_red to get absolute emissions, but then using 2015 Jones data
    region = isEU(region)

    ds_ndc = dsGlobal.GHG_ndc.sel(Region=region)
    ds_ndc_min = ds_ndc.min().values.tolist()
    ds_ndc_max = ds_ndc.max().values.tolist()
    if np.isnan(ds_ndc_min) or np.isnan(ds_ndc_max):
        return None
    return {2030: [ds_ndc_min, ds_ndc_max]}

@app.get("/statistics/ncdProjections/<region>")
def ndcProjections(region):
    return {
        "ndc_inventory": ndcRange_inventory(region),
        "ndc_jones": ndcRange_jones(region)
    }

def get_ds(ISO):
    if ISO not in available_region_files:
        raise ValueError(f"ISO {ISO} not found")
    fn = available_region_files[ISO]
    return xr.open_dataset(fn)


def effortSharing(ISO, principle):
    selection = globalPathwayChoices()
    ds = (get_ds(ISO)[principle]
          .sel(**selection)
          .rename(Time="time")
    )
    # set time as the first dimension
    dim_order = ["time"] + [dim for dim in ds.dims if dim != "time"]
    ds = ds.transpose(*dim_order)

    # extract the 'most reasonable' (mr) df which will be the main trajectory line
    mr_selection = dict()
    if principle in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        mr_selection.update(Scenario="SSP2")
    if principle == "PCC":
        mr_selection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
    if principle in ["ECPC", "GDR"]:
        mr_selection.update(Historical_startyear=DEFAULT_HISTORICAL_STARTYEAR)
    if principle == "ECPC":
        mr_selection.update(Discount_factor=DEFAULT_DISCOUNT_FACTOR,
                            Convergence_year=DEFAULT_CONVERGENCE_YEAR,
                            )
    if principle == "GDR":
        mr_selection.update(RCI_weight=DEFAULT_RCI_WEIGHT,
                            Capability_threshold=DEFAULT_CAPABILITY_THRESHOLD)

    mr_df = ds.sel(**mr_selection).to_pandas().rename("mean")

    if mr_df.isna().all():
        return None

    agg_dims = [dim for dim in ds.dims if dim != "time"]
    min_df = ds.min(agg_dims, skipna=True).to_pandas().rename("min")
    max_df = ds.max(agg_dims, skipna=True).to_pandas().rename("max")

    return (
        pd.concat([mr_df, min_df, max_df], axis=1)
        .reset_index()
        .dropna()
        .to_dict(orient="records")
    )

principles = {"PC", "PCC", "AP", "GDR", "ECPC", "GF"}


@app.get("/timeseries/<region>/principles")
def effortSharings(region):
    """
    http://127.0.0.1:5000//USA/GF?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 36.94ms
    http://127.0.0.1:5000//USA/PC?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 38.556ms
    http://127.0.0.1:5000//USA/PCC?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 37.553ms
    http://127.0.0.1:5000//USA/AP?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 37.296ms
    http://127.0.0.1:5000//USA/GDR?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 37.304ms
    http://127.0.0.1:5000//USA/ECPC?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 10.238ms
    36.94 + 38.56 + 37.55 + 37.29 + 37.30 + 10.23 = 197.869

    http://127.0.0.1:5000//USA/effortSharings?exceedanceRisk=0.67&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 221.552ms
    """
    sharings = {}
    for principle in principles:
        sharing = effortSharing(region, principle)
        if sharing is None:
            continue
        sharings[principle] = sharing
    return sharings


@app.get("/statistics/reductions/<region>")
def effortSharingReductions(region):
    periods = (2030, 2040)
    selection = dict(
        **globalPathwayChoices(),
        Time=periods,
    )

    hist = dsGlobal.GHG_hist.sel(Region=region, Time=1990).values + 0
    ds = get_ds(region)

    reductions = {}
    for principle in principles:
        pselection = selection.copy()
        if principle in ["PC", "PCC", "AP", "GDR", "ECPC"]:
            pselection.update(Scenario="SSP2")
        if principle == "PCC":
            pselection.update(Convergence_year=DEFAULT_CONVERGENCE_YEAR)
        reductions[principle] = {}
        for period in periods:
            pselection.update(Time=period)
            es = ds[principle].sel(**pselection).mean().values + 0
            if np.isnan(es) or np.isnan(hist) or hist == 0:
                reductions[principle][period] = None
            else:
                reductions[principle][period] = -(es - hist) / hist * 100

    return reductions

if __name__ == "__main__":
    print(ndcReductions("USA"))
