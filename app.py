import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px


app = dash.Dash()

server = app.server
df = pd.read_csv("./bp_v_weight_v2.csv",sep=",")

fig_date = px.scatter(df, x="date", y=["bp1","bp2"])
fig_date.update_layout(title="blood pressure over time",xaxis_title="date",yaxis_title="Blood pressure (mmHG)")

fig_weight = px.scatter(df, x="weight (kg)", y=["bp1","bp2"])
fig_weight.update_layout(title="blood pressure versus total weight",xaxis_title="weight (kg)",yaxis_title="Blood pressure (mmHG)")


app.layout = html.Div([
    html.Div([
        dcc.Graph(id='bp1-scatter',
                  figure=fig_date
                  )
                ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bp-weight-scatter',
                  figure=fig_weight
                  )
                ], style={'width': '50%', 'display': 'inline-block'}),

])


if __name__ == '__main__':
    app.run_server(debug=True)