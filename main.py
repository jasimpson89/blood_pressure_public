import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime


def main():
    # Read data from xlxs
    xlsx_file = "/Users/jsimpson/OneDrive/blood_pressure/bp_v_weight_v2.xlsx"
    dfs = pd.read_excel(xlsx_file, sheet_name="new data")
    fig = plot(dfs)
    fig.write_html('first_figure.html', auto_open=True)


def plot(df):
    fig = make_subplots(
        rows=2,cols=1

    )
    fig.add_trace(
        go.Scatter(x=df["date"].tolist(),y=df["bp1"].tolist(),marker='*',line=None),
        row=1,col=1
    )
    fig.add_trace(
        go.Scatter(x=df["date"].tolist(), y=df["bp2"].tolist()),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df["date"].tolist(),y=df["fat mass"].tolist()),
        row=2,col=1
    )

    return fig
main()