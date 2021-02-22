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

fig = px.scatter(df, x="date", y=["bp1","bp2"])


app.layout = html.Div([
    html.Div([
        dcc.Graph(id='bp1-scatter',
                  figure=fig
                  )
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
            dcc.Graph(id='bp2-scatter',
                      figure={
                          'data': [go.Scatter(
                              x=df["date"],
                              y=df["bp2"],

                              mode='markers'
                          )],
                          'layout': go.Layout(
                              title='Bp2 over time',
                              xaxis={'title': 'Date'},
                              yaxis={'title': 'Blood pressure (mmHg)'},
                              hovermode='closest'
                          )}
                      )
        ], style={'width': '50%', 'display': 'inline-block'}),

])


if __name__ == '__main__':
    app.run_server(debug=True)