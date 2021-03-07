import pandas as pd
import numpy as np
import math
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
    # flag used for detecting the first matching index
    first_flag = True


    for month_s,year_s,bp1,bp2,weight_tot in zip(df_monthly_avg.index.month,df_monthly_avg.index.year,df_monthly_avg["systolic"],df_monthly_avg["diastolic"],df_monthly_avg["weight (kg)"]):
        # nan_flag = True
        for date_m, month_m,year_m in zip(df.index, df.index.month,df.index.year):
            if date_m >= df_monthly_avg.index[0] and date_m <= df_monthly_avg.index[-1]:
                if month_s == month_m and year_s == year_m:
                    systolic.append(bp1)
                    diastolic.append(bp2)
                    weight.append(weight_tot)
                    # nan_flag = False
                if first_flag == True:
                    # record this to slice the array with
                    begin_idx = date_m
                    first_flag = False
                else:
                    end_idx = date_m

    # Account for the fact len(df_monthly_avg) could be a different to len(df)
    # The date ranges which 'df_monthly_avg' and 'df' cover maybe different. We only care about months we have BP data for
    df_new = (df[begin_idx:end_idx]).copy()

    """
    ITS STILL FAILING HERE THE LENGTHS OF TH ARARY ARE WRONG 
    """
    df_new['avg monthly systolic'] = systolic
    df_new['avg monthly diastolic'] = diastolic
    df_new['avg monthly weight (kg)'] = weight

    # anything which has NaN can't really be used
    # if any row has a NaN on it get rid of it
    df_new.dropna(axis=0,how='any')

    return df_new
