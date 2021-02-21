import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


#initiating the app
app = dash.Dash()
xlsx_file = "/Users/jsimpson/OneDrive/blood_pressure/bp_v_weight_v2.xlsx"
df = pd.read_excel(xlsx_file, sheet_name="new data")
#defining the layout
app.layout = html.Div([
                html.Div([
                    dcc.Graph(id='mpg-scatter',
                              figure={
                                  'data':[go.Scatter(
                                      x=df['date'],
                                      y=[df['bp1']],
                                      # text=df['name'],
                                      mode='markers'
                                  )],
                                  'layout':go.Layout(
                                      title='MPG vs Model Year',
                                      xaxis={'title':'Model Year'},
                                      yaxis={'title':'MPG'},
                                      hovermode='closest'
                                   )}
                    )
                ],style={'width':'50%','display':'inline-block'}),


])
#running the app
if __name__ == '__main__':
    app.run_server()
