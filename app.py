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
import process_bins
import read_data
import data_process
# https://www.ahajournals.org/doi/epub/10.1161/01.HYP.0000094221.86888.AE ANALYSIS
# Dash requirements
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

server = app.server

# data
df, df_date_strip, df_avg_exercise = read_data.read_csv()
# get monthly average
df_month_avg = data_process.monthly_avg(df)
# match this to the activity
df_avg_exercise = data_process.match_df_month_avg(df_month_avg,df_avg_exercise)


def make_hlines(figure):
    figure.add_hline(y=120, line_dash='dash', line_color='red', opacity=0.25)
    figure.add_hline(y=80, line_dash='dash', line_color='red', opacity=0.25)
    return figure

def drawFigure(dccfigure):
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dccfigure
            ])
        ),
    ])

def drawText(text_title):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(text_title),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])
# Figures
template_plotly = "plotly_dark"
## TAB 1 - raw date plots

fig_fat_mass = px.scatter(df, x="fat mass", y=["systolic","diastolic"],template=template_plotly)
fig_fat_mass.update_layout(title="BP v. fat mass",xaxis_title="fat mass (kg)",yaxis_title="Blood pressure (mmHG)")
fig_fat_mass=make_hlines(fig_fat_mass)

fig_muscle_mass = px.scatter(df, x="muscle mass", y=["systolic","diastolic"],template=template_plotly)
fig_muscle_mass.update_layout(title="BP v. muscle mass",xaxis_title="muscle mass (kg)",yaxis_title="Blood pressure (mmHG)")
fig_muscle_mass=make_hlines(fig_muscle_mass)

fat_percentage = (df["fat mass"]/df["weight (kg)"])*100
df["fat_percentage"] = fat_percentage
fig_fat_percentage = px.scatter(df, x="fat_percentage", y=["systolic","diastolic"],template=template_plotly)
fig_fat_percentage.update_layout(title="BP v. fat percentage",xaxis_title="fat percentage (%)",yaxis_title="Blood pressure (mmHG)")
fig_fat_percentage=make_hlines(fig_fat_percentage)


# TAB 2
df_binned_weight, xtick_bin = process_bins.process_bins(df,'weight (kg)')

fig_binned_weigth = px.scatter(df_binned_weight,x="weight (kg)",y=["systolic","diastolic"],template=template_plotly)
fig_binned_weigth.update_layout(xaxis_title="Total weight binned in 1KG (kg)",yaxis_title="Blood pressure (mmHG)",
                                    xaxis = dict(
                                            tickmode = 'array',
                                            tickvals = df_binned_weight["weight (kg)"],
                                            ticktext = xtick_bin
                                        )
                                )
fig_binned_weigth=make_hlines(fig_binned_weigth)
# MAKE WITH FAT BINNING
df_binned_weight, xtick_bin = process_bins.process_bins(df,'fat mass')
fig_binned_fat_weigth = px.scatter(df_binned_weight,x="fat mass",y=["systolic","diastolic"],template=template_plotly)
fig_binned_fat_weigth.update_layout(xaxis_title="Average fat mass (kg) in bin",yaxis_title="Blood pressure (mmHG)")
fig_binned_fat_weigth=make_hlines(fig_binned_fat_weigth)

df_binned_weight, xtick_bin = process_bins.process_bins(df,'muscle mass')
fig_binned_muscle_weigth = px.scatter(df_binned_weight,x="muscle mass",y=["systolic","diastolic"],template=template_plotly)
fig_binned_muscle_weigth.update_layout(xaxis_title="Average muscle mass (kg) in bin",yaxis_title="Blood pressure (mmHG)")
fig_binned_muscle_weigth=make_hlines(fig_binned_muscle_weigth)

# TAB 3 - exercise


fig_avg_bp_exercise = px.scatter(df_avg_exercise,x="monthly average (h)",y=["avg monthly systolic","avg monthly diastolic"],
                                 template=template_plotly,color=df_avg_exercise.index.month,hover_data=[df_avg_exercise.index.strftime("%d/%m/%Y")])
fig_avg_bp_exercise.update_layout(title="Color show month",xaxis_title="Monthly exerise (hours)",yaxis_title="Blood pressure (mmHG) average of that month")
fig_avg_bp_exercise=make_hlines(fig_avg_bp_exercise)



fig_avg_bp_exercise_color_weight = px.scatter(df_avg_exercise,x="monthly average (h)",y=["avg monthly systolic","avg monthly diastolic"],
                                 template=template_plotly,color='avg monthly weight (kg)',hover_data=[df_avg_exercise.index.strftime("%d/%m/%Y")])
fig_avg_bp_exercise_color_weight.update_layout(xaxis_title="Monthly exerise (hours)",yaxis_title="Blood pressure (mmHG) average of that month")
fig_avg_bp_exercise_color_weight=make_hlines(fig_avg_bp_exercise_color_weight)


app.layout = html.Div([
                dbc.Row(dbc.Col( html.Div(children=[html.H1(children='Blood pressure analysis')]))),
                # dbc.Row(dbc.Col(html.H4("Data over the past year. Conclusion - corelates mostly with weight"))),
                # dbc.Row(dbc.Col(html.H6("Tab 1 - Raw data plots, Tab 2 - plots of some (useful?) analysis, Tab 3 - raw in table form"))),

                dbc.Tabs([
                    dbc.Tab(label='Raw data', children=[
                        dbc.Card([
                            dbc.CardBody([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dbc.Row([
                                                dbc.Col([
                                                    drawText("BP since last appointment"),
                                                        html.Br(),
                                                        html.Div([
                                                        html.H5("Measurements, taken since last appointment (spordically). "
                                                                "Three measurements taken with 1 minute intervals before breakfast."
                                                                " My BP machine could be unreliable taking 4-8 times to get a reading"),
                                                        ],style={'textAlign': 'center'})

                                                ]),


                                                ])
                                           ])
                                        ),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col(
                                            html.Div(["Please select a date to narrow data range. Press X to show all data."],style={'textAlign': 'left'})
                                            , width=3
                                        ),
                                        dbc.Col(
                                            dcc.DatePickerRange(
                                            id='date-picker-range',
                                            start_date="2021/02/01",
                                            end_date=df.index[-1],
                                            start_date_placeholder_text="Start Date",
                                            end_date_placeholder_text="End Date",
                                            calendar_orientation='vertical',
                                            clearable=True,
                                            initial_visible_month="2021/02/01"
                                            )
                                            ,width=4
                                        )
                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            drawFigure(dcc.Graph(id='bp-date-scatter'))
                                        ])
                                    ]),
                                    html.Br(),
                                    dbc.Card(
                                            dbc.CardBody([
                                                dbc.Row([
                                                    dbc.Col([
                                                        drawText("Blood pressure versus weight, this appears to be the main scaling")
                                                    ])])
                                            ])
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        [
                                            dbc.Col(drawFigure(dcc.Graph(id='bp-weight-scatter')), width=8),
                                            dbc.Col([
                                                html.H6('Please use slider below to select total weight range'),
                                                dcc.RangeSlider(
                                                    id='range-slider',
                                                    min=df["weight (kg)"].min(), max=df["weight (kg)"].max(), step=0.1,
                                                    marks={81: '81', 82: '82', 84: '84', 86 : '86', 88: '88'},
                                                    value=[df["weight (kg)"].min(),df["weight (kg)"].max()]
                                                    )
                                            ], width=4)
                                    ]),
                                    html.Br(),
                                    dbc.Card(
                                            dbc.CardBody([
                                                dbc.Row([
                                                    dbc.Col([
                                                        drawText("Interestingly fat percentage doesn't seem to scale the same way")
                                                    ])])
                                            ])
                                    ),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col(drawFigure(dcc.Graph(id='bp-fat-percentage-scatter',figure=fig_fat_percentage)))
                                    ]),
                                html.Br(),
                                dbc.Card(
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                drawText(
                                                    "Total muscle and fat mass need more analysis, see Analysis tab")
                                            ])])
                                    ])
                                ),
                                html.Br(),

                                dbc.Row(
                                        [
                                            dbc.Col(drawFigure(dcc.Graph(id='bp-fat-weight-scatter', figure=fig_fat_mass)),width=6),
                                            dbc.Col(drawFigure(dcc.Graph(id='bp-muscle-weight-scatter', figure=fig_muscle_mass)),width=6),
                                        ]
                                    ,align="centre")
                            ]),
                        ], color="dark"),
                    ]),


                    dbc.Tab(label='Analysis of data', children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("The systolic pressure appears to get close to 120 but rarely exact, accuracy of the machine?"),
                                dbc.Row(
                                    [
                                        dbc.Col(dcc.Graph(id='bp-bin-weight', figure=fig_binned_weigth)),
                                    ]
                                )

                            ]),
                        ]),
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("There appears to be some scaling with binned fat mass"),
                                dbc.Row(
                                    [

                                        dbc.Col(dcc.Graph(id='bp-bin-fat-weight', figure=fig_binned_fat_weigth),width=6),
                                        dbc.Col(dcc.Graph(id='bp-bin-muscle-weight', figure=fig_binned_muscle_weigth),width=6),
                                    ]
                                ),
                            ]),
                        ]),
                    ]),
                    dbc.Tab(label='Exercise', children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("Average exercise per month, shown with average blood pressure for that month"),
                                dbc.Row(
                                    [
                                        dbc.Col(dcc.Graph(id='bp-exercise-avg-bp', figure=fig_avg_bp_exercise),width=6),
                                        dbc.Col(dcc.Graph(id='bp-exercise-avg-bp-color-weight', figure=fig_avg_bp_exercise_color_weight),width=6),

                                    ]
                                ),
                            ]),
                        ])
                    ]),
                    dbc.Tab(label='Data table by date', children=[
                       # Note the dash table is much better but much fiddilier to use
                        dbc.Table.from_dataframe(df_date_strip, striped=True, bordered=True, hover=True)

                    ]),
                    dbc.Tab(label='Data table weight', children=[
                       # Note the dash table is much better but much fiddilier to use
                        dbc.Table.from_dataframe(df_date_strip.sort_values(by='weight (kg)'), striped=True, bordered=True, hover=True)

                    ])
                ])
            ])

# Call back for plot 1 of date select date range
@app.callback(
    dash.dependencies.Output('bp-date-scatter', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date')]
)
def figupdate(start_date, end_date):

    filtered_df = df.loc[start_date:end_date]


    figure = px.scatter(filtered_df, x=filtered_df.index, y=["systolic","diastolic"],hover_data= ["weight (kg)","comments"],template=template_plotly)
    figure.update_layout({'xaxis':{'tickformat': '%d/%m/%y'}},title="BP over time",xaxis_title="date",yaxis_title="Blood pressure (mmHG)",
                       hovermode="x unified")
    figure=make_hlines(figure)

    return figure


# call back for slider for weight (kg) range
@app.callback(
    Output("bp-weight-scatter", "figure"),
    [Input("range-slider", "value")])
def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (df['weight (kg)'] > low) & (df['weight (kg)'] < high)

    fig_weight = px.scatter(df[mask], x="weight (kg)", y=["systolic", "diastolic"], template=template_plotly)
    fig_weight.update_layout(title="BP v. total weight", xaxis_title="weight (kg)", yaxis_title="Blood pressure (mmHG)")
    fig_weight = make_hlines(fig_weight)

    return fig_weight


if __name__ == '__main__':
    app.run_server(debug=True)