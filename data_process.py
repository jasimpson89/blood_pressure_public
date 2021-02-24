import pandas as pd
import numpy as np

def monthly_avg(df):
    # this generates a group object, this groups byn month/year (i.e. both) if you wanted to group on months across many
    # years you would need something else
    g = df.groupby(pd.Grouper(freq='M'))
    # takes the mean on this group
    df_month_avg = g.mean()
    return df_month_avg

def match_df_month_avg(df_monthly_avg,df):
    """

    :param df_monthly_avg: takes the data frame and matches the date in df
    :param df: adds an new column to df to have the systolic and diastolic month averages
    :return: df
    """
    # theres defo a faster way of doing this
    systolic = []
    diastolic = []
    weight = []
    for month_s,year_s,bp1,bp2,weight_tot in zip(df_monthly_avg.index.month,df_monthly_avg.index.year,df_monthly_avg["systolic"],df_monthly_avg["diastolic"],df_monthly_avg["weight (kg)"]):
        for month_m,year_m in zip(df.index.month,df.index.year):
            if month_s == month_m and year_s == year_m:
                systolic.append(bp1)
                diastolic.append(bp2)
                weight.append(weight_tot)
                continue


    df['avg monthly systolic'] = systolic
    df['avg monthly diastolic'] = diastolic
    df['avg monthly weight (kg)'] = weight

    # anything which has NaN can't really be used
    # if any row has a NaN on it get rid of it
    df.dropna(axis=0,how='any')

    return df
