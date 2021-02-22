import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


app = dash.Dash()

server = app.server
df = pd.read_csv("./bp_v_weight_v2.csv",sep=",")



app.layout = html.Div([
    html.Div([
        dcc.Graph(id='bp1-scatter',
                  figure={
                      'data': [go.Scatter(
                          x=df["date"],
                          y=df["bp1"],

                          mode='markers'
                      )],
                      'layout': go.Layout(
                          title='Bp1 over time',
                          xaxis={'title': 'Date'},
                          yaxis={'title': 'Blood pressure (mmHg)'},
                          hovermode='closest'
                      )}
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