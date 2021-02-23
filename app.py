import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import datetime as dt
# https://www.ahajournals.org/doi/epub/10.1161/01.HYP.0000094221.86888.AE ANALYSIS
# Dash requirements
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

server = app.server

# Pandas
df = pd.read_csv("./bp_v_weight_v2.csv",sep=",")
# convert the date to date time object in pandas
df_date_strip = df.copy(deep=True)
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
df.set_index('date', inplace=True)


# Figures

# this is dealt with in the update function
# figure=fig_date = px.scatter(df, x=df.index, y=["systolic","diastolic"],hover_data= ["weight (kg)","comments"],template="plotly_dark")
# fig_date.update_layout({'xaxis':{'tickformat': '%d/%m'}},title="BP over time",xaxis_title="date",yaxis_title="Blood pressure (mmHG)",
#                        hovermode="x unified")

## TAB 1 - raw date plots
fig_weight = px.scatter(df, x="weight (kg)", y=["systolic","diastolic"],template="plotly_dark")
fig_weight.update_layout(title="BP v. total weight",xaxis_title="weight (kg)",yaxis_title="Blood pressure (mmHG)")

fig_fat_mass = px.scatter(df, x="fat mass", y=["systolic","diastolic"],template="plotly_dark")
fig_fat_mass.update_layout(title="BP v. fat mass",xaxis_title="fat mass (kg)",yaxis_title="Blood pressure (mmHG)")

fig_muscle_mass = px.scatter(df, x="muscle mass", y=["systolic","diastolic"],template="plotly_dark")
fig_muscle_mass.update_layout(title="BP v. muscle mass",xaxis_title="muscle mass (kg)",yaxis_title="Blood pressure (mmHG)")

fat_percentage = (df["fat mass"]/df["weight (kg)"])*100
df["fat_percentage"] = fat_percentage
fig_fat_percentage = px.scatter(df, x="fat_percentage", y=["systolic","diastolic"],template="plotly_dark")
fig_fat_percentage.update_layout(title="BP v. fat percentage",xaxis_title="fat percentage (%)",yaxis_title="Blood pressure (mmHG)")


## TABS 2 - analysis
df.groupby


app.layout = html.Div([
                dbc.Row(dbc.Col(html.H1("Blood pressure analysis"))),
                dbc.Row(dbc.Col(html.H4("Data over the past year. Conclusion - corelates mostly with weight"))),
                dbc.Row(dbc.Col(html.H6("Tab 1 - Raw data plots, Tab 2 - plots of some (useful?) analysis, Tab 3 - raw in table form"))),

                dbc.Tabs([
                    dbc.Tab(label='Raw data', children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.CardBody([
                                            html.H5("Blood pressure recorded (sporadically) since last appointment. "
                                                    "Took 3 measurements with 1 minute intervals. "
                                                    "The monitor used was not particular reliable."),
                                            dcc.DatePickerRange(
                                                id='date-picker-range',
                                                start_date=df.index[0],
                                                end_date=df.index[-1],
                                                start_date_placeholder_text="Start Date",
                                                end_date_placeholder_text="End Date",
                                                calendar_orientation='vertical',
                                                clearable=True,
                                                initial_visible_month="2021/02/01"
                                            ),
                                            html.H6("Please select a date to narrow data range"),
                                            dcc.Graph(id='bp-date-scatter')
                                        ]),
                                ]),
                            ]),
                            dbc.Card([
                                dbc.CardBody([
                                        html.H5("Blood pressure versus weight, this appears to be the main scaling"),
                                        dbc.Col(dcc.Graph(id='bp-weight-scatter',figure=fig_weight))
                                ]),
                            ]),
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='bp-fat-percentage-scatter',figure=fig_fat_percentage)
                                ]),
                            ]),
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row(
                                        [
                                            dbc.Col(dcc.Graph(id='bp-fat-weight-scatter', figure=fig_fat_mass)),
                                            dbc.Col(dcc.Graph(id='bp-muscle-weight-scatter', figure=fig_muscle_mass)),
                                        ]
                                    ),
                                ]),
                            ]),

                        ]),
                    dbc.Tab(label='Data table', children=[
                        dbc.Table.from_dataframe(df_date_strip, striped=True, bordered=True, hover=True)
                        # dash_table.DataTable(
                        #     id='table',
                        #     style_cell = {'whiteSpace': 'normal','height': 'auto'},
                        #     columns=[{"name": i, "id": i} for i in df.columns],
                        #     data=df.to_dict('records'),
                        #     style_data_conditional=[
                        #         {
                        #             'if': {
                        #                 'column_id': 'systolic',
                        #             },
                        #             'backgroundColor': 'dodgerblue',
                        #             'color': 'white'
                        #         },
                        #         {
                        #             'if': {
                        #                 'column_id': 'diastolic',
                        #             },
                        #             'backgroundColor': 'red',
                        #             'color': 'white'
                        #         },
                        #     ]
                        # )
                    ])
                ])
            ])


@app.callback(
    dash.dependencies.Output('bp-date-scatter', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date')]
)
def figupdate(start_date, end_date):

    filtered_df = df.loc[start_date:end_date]


    figure = px.scatter(filtered_df, x=filtered_df.index, y=["systolic","diastolic"],hover_data= ["weight (kg)","comments"],template="plotly_dark")
    figure.update_layout({'xaxis':{'tickformat': '%d/%m/%y'}},title="BP over time",xaxis_title="date",yaxis_title="Blood pressure (mmHG)",
                       hovermode="x unified")

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)