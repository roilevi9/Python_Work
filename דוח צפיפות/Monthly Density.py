import pandas as pd
import numpy as np
from datetime import datetime


df = pd.read_excel("C:\\Users\\roil\\Downloads\\Density April.xlsx", parse_dates=["תאריך"])
df_new = df

# Sort Data:
column_names = ['RecordID', 'Matrix', 'Reviewer Name', 'Date', 'Time', 'Destination', 'The Herzl Segment', 'Air Force Segment', 'Leading Trailer', 'Sampling Time', 'First Car Weight', 'Second Car Weight', 'Comments']
df_new.columns = column_names

def to_israeli_date(d):
    date = datetime.strptime(d, '%d/%m/%Y')
    return date.strftime('%d.%m.%Y')

df_new['Date'] = df_new.Date.apply(to_israeli_date)
df_new['Time'] = pd.to_datetime(df_new['Time'], format='%H:%M:%S')
df_new["Sampling Time"] = pd.to_datetime(df_new["Sampling Time"], format='%H:%M:%S')


df_new['First Car Weight'].fillna(df_new['Second Car Weight'], inplace=True)
df_new['Second Car Weight'].fillna(df_new['First Car Weight'], inplace=True)

df_new.loc[df['First Car Weight'].isna(), 'Second Car Weight'] = df_new['First Car Weight']
df_new.loc[df['Second Car Weight'].isna(), 'First Car Weight'] = df_new['Second Car Weight']

df.loc[df['First Car Weight'] > 100, 'First Car Weight'] = np.nan
df.loc[df['Second Car Weight'] > 100, 'Second Car Weight'] = np.nan
df.loc[df['First Car Weight'] == 0, 'First Car Weight'] = np.nan
df.loc[df['Second Car Weight'] == 0, 'Second Car Weight'] = np.nan
df_new.dropna(subset=['First Car Weight', 'Second Car Weight'], how='all', inplace=True)

df_new["Section"] = df_new["Air Force Segment"].fillna(df_new["The Herzl Segment"])

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


df_new['time_range'] = df_new['Sampling Time'].apply(get_time_range)

df_new.drop(['Air Force Segment', 'The Herzl Segment', "Comments", "Matrix", "Reviewer Name"], axis=1, inplace=True)
df_new.reset_index(drop=True)

# Data Processing:
Alpha_Model_1 = 6.7525
Alpha_Model_2 = -19.072
Beta_Model_1 = 0.8893
Beta_Model_2 = 1.1707
Seats_Per_Car = 56
Standing = 34.5314
dev = 2.75

df_new["Conversion First Car"] = df_new["First Car Weight"] * 3.1
df_new["Model First Car"] = np.where(df_new["Conversion First Car"] < 120, df_new["Conversion First Car"] * Beta_Model_1 + Alpha_Model_1, df_new["Conversion First Car"] * Beta_Model_2 + Alpha_Model_2)
df_new["Conversion Second Car"] = df_new["Second Car Weight"] * 3.1
df_new["Model Second Car"] = np.where(df_new["Conversion Second Car"] < 120, df_new["Conversion Second Car"] * Beta_Model_1 + Alpha_Model_1, df_new["Conversion Second Car"] * Beta_Model_2 + Alpha_Model_2)
df_new["Weight First Car"] = df_new["Model First Car"] / 3.1
df_new["Weight Second Car"] = df_new["Model Second Car"] / 3.1
df_new["Number Of Passengers"] = df_new["Model First Car"] + df_new["Model Second Car"]
df_new["T1"] = np.where((df_new["Model First Car"]-Seats_Per_Car) > 0, (df_new["Model First Car"]-Seats_Per_Car)/Standing, 0)
df_new["T2"] = np.where((df_new["Model Second Car"]-Seats_Per_Car) > 0, (df_new["Model Second Car"]-Seats_Per_Car)/Standing, 0)
df_new["DEV"] = np.where((df_new["T1"] > dev) | (df_new["T2"] > dev), 1, 0)

pivot_table = pd.pivot_table(df_new, values="DEV", index='Date', columns=['time_range', 'Section'], aggfunc=np.sum, fill_value=0)
print(pivot_table)

writer = pd.ExcelWriter('New Density April.xlsx', engine='xlsxwriter')
df_new.to_excel(writer, sheet_name="Calculation Person Per Meter", index=False)
pivot_table.to_excel(writer, sheet_name="Deviation Pivot table")
writer.close()


#print(df_new.head(10))
# print()
# print(df_new[['DEV']].sum())
# print(df_new[['Model First Car']].sum())
# print(df_new[['Model Second Car']].sum())
# print(df_new[['RecordID']].count())
# print()
# print(df_new[['First Car Weight', 'Second Car Weight']].max())
# print()
# print(df_new[['First Car Weight', 'Second Car Weight']].min())
