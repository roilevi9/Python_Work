import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_excel("All Records Of Cfir.xlsx", parse_dates=["תאריך"])


# Sort Data:
column_names = ['RecordID', 'Matrix', 'Reviewer Name', 'Date', 'Time', 'Destination', 'The Herzl Segment', 'Air Force Segment', 'Leading Trailer', 'Sampling Time', 'First Car Weight', 'Second Car Weight', 'Comments']
df.columns = column_names

df.loc[df['Reviewer Name'] == 'Simon', 'Reviewer Name'] = np.nan
df.loc[df['Reviewer Name'] == 'Yaron', 'Reviewer Name'] = np.nan
df.dropna(subset=['First Car Weight', 'Second Car Weight'], how='all', inplace=True)

print(df.head(), "\n")

df['only time'] = pd.to_datetime(df['Sampling Time'], errors='coerce').dt.time
df['Sampling Time'] = df.apply(lambda row: row['only time'] if len(row['Sampling Time']) > 8 else row['Sampling Time'], axis=1)
df.drop('only time', axis=1, inplace=True)
df.reset_index(drop=True)

def to_israeli_date(d):
    date = datetime.strptime(d, '%d/%m/%Y')
    return date.strftime('%d.%m.%Y')


df['Date'] = df.Date.apply(to_israeli_date)
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
df["Sampling Time"] = pd.to_datetime(df["Sampling Time"], format='%H:%M:%S')

df['First Car Weight'].fillna(df['Second Car Weight'], inplace=True)
df['Second Car Weight'].fillna(df['First Car Weight'], inplace=True)

df.loc[df['First Car Weight'].isna(), 'Second Car Weight'] = df['First Car Weight']
df.loc[df['Second Car Weight'].isna(), 'First Car Weight'] = df['Second Car Weight']

df.loc[df['First Car Weight'] > 100, 'First Car Weight'] = np.nan
df.loc[df['Second Car Weight'] > 100, 'Second Car Weight'] = np.nan
df.loc[df['First Car Weight'] == 0, 'First Car Weight'] = np.nan
df.loc[df['Second Car Weight'] == 0, 'Second Car Weight'] = np.nan
df.dropna(subset=['First Car Weight', 'Second Car Weight'], how='all', inplace=True)

df["Section"] = df["Air Force Segment"].fillna(df["The Herzl Segment"])

def get_time_range(hour_str):
    hour = pd.to_datetime(hour_str).time()
    if hour >= pd.to_datetime('00:00').time() and hour < pd.to_datetime('01:00').time():
        return '00:00-1:00'
    elif hour >= pd.to_datetime('01:00').time() and hour < pd.to_datetime('02:00').time():
        return '01:00-02:00'
    elif hour >= pd.to_datetime('02:00').time() and hour < pd.to_datetime('03:00').time():
        return '02:00-03:00'
    elif hour >= pd.to_datetime('03:00').time() and hour < pd.to_datetime('04:00').time():
        return '03:00-04:00'
    elif hour >= pd.to_datetime('04:00').time() and hour < pd.to_datetime('05:00').time():
        return '04:00-05:00'
    elif hour >= pd.to_datetime('05:00').time() and hour < pd.to_datetime('06:00').time():
        return '05:00-06:00'
    elif hour >= pd.to_datetime('06:00').time() and hour < pd.to_datetime('07:00').time():
        return '06:00-07:00'
    elif hour >= pd.to_datetime('07:00').time() and hour < pd.to_datetime('08:00').time():
        return '07:00-08:00'
    elif hour >= pd.to_datetime('08:00').time() and hour < pd.to_datetime('09:00').time():
        return '08:00-09:00'
    elif hour >= pd.to_datetime('09:00').time() and hour < pd.to_datetime('10:00').time():
        return '09:00-10:00'
    elif hour >= pd.to_datetime('10:00').time() and hour < pd.to_datetime('11:00').time():
        return '10:00-11:00'
    elif hour >= pd.to_datetime('11:00').time() and hour < pd.to_datetime('12:00').time():
        return '11:00-12:00'
    elif hour >= pd.to_datetime('12:00').time() and hour < pd.to_datetime('13:00').time():
        return '12:00-13:00'
    elif hour >= pd.to_datetime('13:00').time() and hour < pd.to_datetime('14:00').time():
        return '13:00-14:00'
    elif hour >= pd.to_datetime('14:00').time() and hour < pd.to_datetime('15:00').time():
        return '14:00-15:00'
    elif hour >= pd.to_datetime('15:00').time() and hour < pd.to_datetime('16:00').time():
        return '15:00-16:00'
    elif hour >= pd.to_datetime('16:00').time() and hour < pd.to_datetime('17:00').time():
        return '16:00-17:00'
    elif hour >= pd.to_datetime('17:00').time() and hour < pd.to_datetime('18:00').time():
        return '17:00-18:00'
    elif hour >= pd.to_datetime('18:00').time() and hour < pd.to_datetime('19:00').time():
        return '18:00-19:00'
    elif hour >= pd.to_datetime('19:00').time() and hour < pd.to_datetime('20:00').time():
        return '19:00-20:00'
    elif hour >= pd.to_datetime('20:00').time() and hour < pd.to_datetime('21:00').time():
        return '20:00-21:00'
    elif hour >= pd.to_datetime('21:00').time() and hour < pd.to_datetime('22:00').time():
        return '21:00-22:00'
    elif hour >= pd.to_datetime('22:00').time() and hour < pd.to_datetime('23:00').time():
        return '22:00-23:00'
    else:
        return '23:00-0:00'


df['time_range'] = df['Sampling Time'].apply(get_time_range)

df.drop(['Air Force Segment', 'The Herzl Segment', "Comments", "Matrix", "Reviewer Name"], axis=1, inplace=True)
df.reset_index(drop=True)

print(df.head())
