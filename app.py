import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

#initiating the app
app = dash.Dash()
server = app.server

xlsx_file = "/Users/jsimpson/OneDrive/blood_pressure/bp_v_weight_v2.xlsx"
df = pd.read_excel(xlsx_file, sheet_name="new data")


app.layout = html.Div([
                html.Div([
                    dcc.Graph(id='mpg-scatter',
                              figure={
                                  'data':[go.Scatter(
                                      x=df['date'],
                                      y=df['bp1'],

                                      mode='markers'
                                  )],
                                  'layout':go.Layout(
                                      title='Bp1 over time',
                                      xaxis={'title':'Date'},
                                      yaxis={'title':'Blood pressure (mmHg)'},
                                      hovermode='closest'
                                   )}
                    )
                ],style={'width':'50%','display':'inline-block'}),
])
if __name__ == '__main__':


    app.run_server()