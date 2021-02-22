import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

# https://www.ahajournals.org/doi/epub/10.1161/01.HYP.0000094221.86888.AE ANALYSIS
# Dash requirements
app = dash.Dash()
server = app.server

# Pandas
df = pd.read_csv("./bp_v_weight_v2.csv",sep=",")
# convert the date to date time object in pandas
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')


# Figures
fig_date = px.scatter(df, x="date", y=["systolic","diastolic"],hover_data= ["weight (kg)","comments"])
fig_date.update_layout({'xaxis':{'tickformat': '%d/%m'}},title="BP over time",xaxis_title="date",yaxis_title="Blood pressure (mmHG)",
                       hovermode="x unified")


fig_weight = px.scatter(df, x="weight (kg)", y=["systolic","diastolic"])
fig_weight.update_layout(title="BP v. total weight",xaxis_title="weight (kg)",yaxis_title="Blood pressure (mmHG)")

fig_fat_mass = px.scatter(df, x="fat mass", y=["systolic","diastolic"])
fig_fat_mass.update_layout(title="BP v. fat mass",xaxis_title="fat mass (kg)",yaxis_title="Blood pressure (mmHG)")

fig_muscle_mass = px.scatter(df, x="muscle mass", y=["systolic","diastolic"])
fig_muscle_mass.update_layout(title="BP v. muscle mass",xaxis_title="muscle mass (kg)",yaxis_title="Blood pressure (mmHG)")

fat_percentage = (df["fat mass"]/df["weight (kg)"])*100
df["fat_percentage"] = fat_percentage
fig_fat_percentage = px.scatter(df, x="fat_percentage", y=["systolic","diastolic"])
fig_fat_percentage.update_layout(title="BP v. fat percentage",xaxis_title="fat percentage (%)",yaxis_title="Blood pressure (mmHG)")


app.layout = html.Div([
    html.Div([
        dcc.Graph(id='bp-date-scatter',
                  figure=fig_date
                  )
    ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bp-weight-scatter',
                  figure=fig_weight
                  )
                ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bp-fat-weight-scatter',
                  figure=fig_fat_mass
                  )
                ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='bp-muscle-weight-scatter',
                  figure=fig_muscle_mass
                  )
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bp-fat-percentage-scatter',
                  figure=fig_fat_percentage
                  )
    ], style={'width': '50%', 'display': 'inline-block'}),

])


if __name__ == '__main__':
    app.run_server(debug=True)