import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


app = dash.Dash()

server = app.server
url="https://github.com/jasimpson89/blood_pressure/blob/master/bp_v_weight_v2.csv"
df = df = pd.read_csv(url,sep=",")
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='mpg-scatter',
                  figure={
                      'data': [go.Scatter(
                          x=[1,2,3],
                          y=[10,20,30],

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

])


if __name__ == '__main__':
    app.run_server(debug=True)