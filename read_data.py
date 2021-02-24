import pandas as pd

def read_csv():
    # Pandas
    df = pd.read_csv("./bp_v_weight_v2.csv", sep=",")
    df.rename(columns={"bp1": "systolic", "bp2": "diastolic"}, inplace=True)
    # convert the date to date time object in pandas

    df_date_strip = df.copy(deep=True)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df.set_index('date', inplace=True)

    df_avg_exercise = pd.read_csv("./average_exercise.csv", sep=",")
    df_avg_exercise['date'] = pd.to_datetime(df_avg_exercise['date'], format='%d/%m/%Y')
    df_avg_exercise.set_index('date', inplace=True)

    return df, df_date_strip, df_avg_exercise