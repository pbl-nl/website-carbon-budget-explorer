"""

Install with

    pip install flask gunicorn

Run with

    gunicorn -w 4 'ws:app'

"""

import xarray as xr

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# TODO improve endpoint names
# TODO use class-based views for a reusable nc-file viewer?
# TODO write tests with dummy data
# TODO validate inputs? Must if ws is public

# Global data (xr_dataread.nc)
dsGlobal = xr.open_dataset("data/xr_dataread.nc")

@app.get("/pathwayCarbon")
def pathwayCarbon():
    """Get global carbon pathway for a given selection.

    To test:
    production server:
    http://127.0.0.1:8000/pathwayCarbon?nonCO2Mitigation=0.5&exceedanceRisk=0.5&negativeEmissions=0.5

    dev server:
    http://127.0.0.1:5000/pathwayCarbon?nonCO2Mitigation=0.5&exceedanceRisk=0.5&negativeEmissions=0.5
    """
    df = (
        dsGlobal.CO2_globe.sel(
            # TODO remove defaults
            # TODO use request.data instead of request.args?
            # args uses GET, data uses POST, GET is idempotent which is easier to cache so keep using args
            **pathwaySelection(),
            Time=slice(2021, 2100),
        )
        .rename({"Time": "time"})
        .to_pandas()
    )
    return (
        df.agg(func=["min", "mean", "max"])
        .transpose()
        .reset_index()
        .to_dict(orient="records")
    )


@app.get("/pathwayChoices")
def pathwayChoices():
    return {
        "temperature": dsGlobal.Temperature.values.tolist(),
        "exceedanceRisk": dsGlobal.Risk.values.tolist(),
        "nonCO2Mitigation": dsGlobal.NonCO2.values.tolist(),
        "negativeEmissions": dsGlobal.NegEmis.values.tolist(),
    }


def pathwaySelection():
    choices = pathwayChoices()
    defaults = {k: v[len(v) // 2] for k, v in choices.items()}
    return dict(
        Temperature=request.args.get("temperature", defaults["temperature"]),
        Risk=request.args.get("exceedanceRisk", defaults["exceedanceRisk"]),
        NegEmis=request.args.get("negativeEmissions", defaults["negativeEmissions"]),
        NonCO2=request.args.get("nonCO2Mitigation", defaults["nonCO2Mitigation"]),
    )


@app.get("/regions")
def regions():
    return dsGlobal.Region.values.tolist()


@app.get("/pathwayStats")
def pathwayStats():
    used = dsGlobal.CO2_hist.sel(Region="WORLD").sum().values.tolist()
    remaining = (
        dsGlobal.CO2_globe.sel(
            TrajUnc="Medium",
            **pathwaySelection(),
        )
        .sum()
        .values.tolist()
    )
    total = used + remaining

    return {"total": total, "used": used, "remaining": remaining}


@app.get("/historicalCarbon/<region>")
def historicalCarbon(region="WORLD"):
    start = request.args.get("start")
    end = request.args.get("end")
    df = dsGlobal.CO2_hist.sel(
        Region=region, Time=slice(start, end)
    ).to_pandas()
    df.index.rename("time", True)
    df = df.reset_index()
    df["value"] = df.pop(0)
    return df.to_dict(orient="records")


@app.get("/populationOverTime/<region>")
def populationOverTime(region):
    start = request.args.get("start")
    end = request.args.get("end")
    scenario = "SSP2"
    df = dsGlobal.Population.sel(
        Scenario=scenario, Region=region, Time=slice(start, end)
    ).to_pandas()
    df.index.rename("time", True)
    df = df.dropna().reset_index()  # Note the missing data!
    df["value"] = df.pop(0)
    return df.to_dict(orient="records")


@app.get("/gdpOverTime/<region>")
def gdpOverTime(region):
    start = request.args.get("start")
    end = request.args.get("end")
    scenario = "SSP2"
    df = dsGlobal.Population.sel(
        Scenario=scenario, Region=region, Time=slice(start, end)
    ).to_pandas()
    df.index.rename("time", True)
    df = df.dropna().reset_index()  # Note the missing data!
    df["value"] = df.pop(0)
    return df.to_dict(orient="records")


# Map data (xr_alloc_2030.nc etc)
ds_alloc_2030 = xr.open_dataset("data/xr_alloc_2030.nc")
# ds_alloc_2040 = xr.open_dataset("data/xr_alloc_2040.nc")


@app.get("/fullCenturyBudgetSpatial")
def fullCenturyBudgetSpatial():
    effortSharing = request.args.get("effortSharing", "PCC")
    selection = dict(
        **pathwaySelection()
    )
    if effortSharing in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        selection.update(Scenario="SSP2")
    if effortSharing == "PCC":
        selection.update(Convergence_year=2040)

    # TODO make it possible to choose 2040
    df = ds_alloc_2030[effortSharing].sel(**selection).to_pandas()

    # Taking mean over TrajUnc dimension
    # TODO should we pin TrajUnc to a specific value? Or take max or min?
    df = df.agg(func="mean", axis=1).dropna()  # Note: dropping nan values here

    # Index is called Region and column is unnamed
    df.index.rename("ISO", True)
    df = df.reset_index()
    df["value"] = df.pop(0)
    return df.to_dict(orient="records")


# Reference pathway data (xr_policyscen.nc)
ds_policyscen = xr.open_dataset("data/xr_policyscen.nc")


@app.get("/policyPathway/<policy>/<region>")
def policyPathway(policy, region):
    policy_ds = (
        ds_policyscen[policy]
        .sel(Region=region, Time=slice(2021, 2100))
        .drop("Region")
        .groupby("Time")
    )

    # TODO precompute mean, min and max
    # instead of calculating them on the fly each time
    df = xr.merge(
        [
            policy_ds.mean(["Model"]).rename("mean"),
            policy_ds.min(["Model"]).rename("min"),
            policy_ds.max(["Model"]).rename("max"),
        ]
    ).to_pandas()
    df.index.rename("time", True)
    return df.reset_index().to_dict(orient="records")


# Country-specific data (xr_alloc_<ISO>.nc)


def get_ds(ISO):
    return xr.open_dataset(f"data/xr_alloc_{ISO}.nc")


@app.get("/<ISO>/<principle>")
def effortSharing(ISO, principle):
    selection = dict(
        **pathwaySelection(),
    )

    # TODO should I do aggregation on Scenario and Convergence_year?
    # or use static selection?
    if principle in ["PC", "PCC", "AP", "GDR", "ECPC"]:
        selection.update(Scenario="SSP2")
    if principle == "PCC":
        selection.update(Convergence_year=2040)

    ds = get_ds(ISO)[principle].sel(**selection)
    if principle == "ECPC":
        uncertainty = (
            ds.to_pandas().agg(["mean", "min", "max"]).transpose().to_dict()
        )
        return [
            {"time": 2100, **uncertainty},
        ]
    else:
        df = ds.rename(Time="time").to_pandas()
        if principle in ["GF", "PC"]:
            # These effort sharing principles have Time dimension after TrajUnc dimension
            # While all other principles have TrajUnc dimension after Time dimension
            # Causing columns to be Time and TrajUnc to be rows in dataframe
            # We want the opposite
            # TODO order dimensions for each principle in same way, so this is not needed anymore

            df = df.transpose()

        return (
            df.agg(["mean", "min", "max"], axis=1)
            .reset_index()
            .to_dict(orient="records")
        )

@app.get("/<ISO>/effortSharings")
def effortSharings(ISO):
    """
http://127.0.0.1:5000//USA/GF?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 36.94ms
http://127.0.0.1:5000//USA/PC?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 38.556ms
http://127.0.0.1:5000//USA/PCC?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 37.553ms
http://127.0.0.1:5000//USA/AP?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 37.296ms
http://127.0.0.1:5000//USA/GDR?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 37.304ms
http://127.0.0.1:5000//USA/ECPC?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 10.238ms
36.94 + 38.56 + 37.55 + 37.29 + 37.30 + 10.23 = 197.869

http://127.0.0.1:5000//USA/effortSharings?exceedanceRisk=0.67&nonCO2Mitigation=0.2&negativeEmissions=0.4&effortSharing=PCC&temperature=1.8: 221.552ms
    """
    principles = ["PC", "PCC", "AP", "GDR", "ECPC", "GF"]
    return {k: effortSharing(ISO, k) for k in principles}