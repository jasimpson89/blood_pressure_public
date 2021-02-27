import pandas as pd
import base64
def create_onedrive_directdownload (onedrive_link):
    """
    Found here - https://towardsdatascience.com/how-to-get-onedrive-direct-download-link-ecb52a62fee4

    This is the only  way I was able to directly read my datafrom onedrive using a share link

    :param onedrive_link:
    :return:
    """
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl
def read_csv():
    """
    Description - reads data in to pandas datafrmes, directly from my onedrive
    :return:
    df - pandas df which has all the blood pressure and weight data in it
    df_date_strip - probably not needed, a copy of df with time stripeed out of datatime so it looks nice in the table format
    df_avg_exercise - contains data in dataframe of the average exercise
    """

    # Read blood pressure data
    blood_pressure_path = 'https://1drv.ms/u/s!ArlllFGoorx2hINGANQzDmW1QHwn3g?e=t8zhWT'
    bp_load_url = create_onedrive_directdownload(blood_pressure_path)
    df = pd.read_csv(bp_load_url)
    # Rename columns
    df.rename(columns={"bp1": "systolic", "bp2": "diastolic"}, inplace=True)

    # convert the date to date time object in pandas
    df_date_strip = df.copy(deep=True)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df.set_index('date', inplace=True)

    # Read average exercise data
    average_exercise_path = 'https://1drv.ms/u/s!ArlllFGoorx2hINH2WLsOhWqqXLuMw?e=N7K2I4'
    average_exercise_url = create_onedrive_directdownload(average_exercise_path)
    df_avg_exercise = pd.read_csv(average_exercise_url, sep=",")
    df_avg_exercise['date'] = pd.to_datetime(df_avg_exercise['date'], format='%d/%m/%Y')
    df_avg_exercise.set_index('date', inplace=True)

    return df, df_date_strip, df_avg_exercise

