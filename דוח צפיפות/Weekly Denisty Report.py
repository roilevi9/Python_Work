import pandas as pd
import numpy as np


df = pd.read_excel("C:\\Users\\roil\\Downloads\\Weekly Density 21-27.5.xlsx", parse_dates=["תאריך"])
df_new = df

# Sort Data:
column_names = ['RecordID', 'Matrix', 'Reviewer Name', 'Date', 'Time', 'Destination', 'The Herzl Segment', 'Air Force Segment', 'Leading Trailer', 'Sampling Time', 'First Car Weight', 'Second Car Weight', 'Comments']
df_new.columns = column_names

def to_israeli_date(d):
  date = d.to_pydatetime()
  day   = date.day
  month = date.month
  year  = date.year
  return '%s.%s.%s' % (day, month, year)

df_new['Date'] = df_new.Date.apply(to_israeli_date)
df_new['Time'] = pd.to_datetime(df_new['Time'], format='%H:%M:%S')
df_new["Sampling Time"] = pd.to_datetime(df_new["Sampling Time"], format='%H:%M:%S')


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

df.loc[df['First Car Weight'] == 0, 'First Car Weight'] = np.nan
df.loc[df['Second Car Weight'] == 0, 'Second Car Weight'] = np.nan
df.loc[df['First Car Weight'] > 100, 'First Car Weight'] = np.nan
df.loc[df['Second Car Weight'] > 100, 'Second Car Weight'] = np.nan
df_new.dropna(subset=["First Car Weight"], inplace=True)
df_new.dropna(subset=["Second Car Weight"], inplace=True)
df_new["Section"] = df_new["Air Force Segment"].fillna(df_new["The Herzl Segment"])
df_new.drop(['Air Force Segment', 'The Herzl Segment', "Comments", "Matrix", "Reviewer Name"], axis=1, inplace=True)
df_new.reset_index(drop=True)

# Data Processing:
Alpha_Model_1 = 6.7525
Alpha_Model_2 = -19.072
Beta_Model_1 = 0.8893
Beta_Model_2 = 1.1707
df_new["Conversion First Car"] = df_new["First Car Weight"] * 3.1
df_new["Model First Car"] = np.where(df_new["Conversion First Car"] < 120, df_new["Conversion First Car"] * Beta_Model_1 + Alpha_Model_1, df_new["Conversion First Car"] * Beta_Model_2 + Alpha_Model_2)
df_new["Conversion Second Car"] = df_new["Second Car Weight"] * 3.1
df_new["Model Second Car"] = np.where(df_new["Conversion Second Car"] < 120, df_new["Conversion Second Car"] * Beta_Model_1 + Alpha_Model_1, df_new["Conversion Second Car"] * Beta_Model_2 + Alpha_Model_2)
df_new["Weight First Car"] = df_new["Model First Car"] / 3.1
df_new["Weight Second Car"] = df_new["Model Second Car"] / 3.1
df_new["Number Of Passengers"] = df_new["Model First Car"] + df_new["Model Second Car"]

pivot_table = pd.pivot_table(df_new, values="Number Of Passengers", index=['Destination', 'Section'], columns='time_range', aggfunc=np.max, fill_value=0)
print(pivot_table)


writer = pd.ExcelWriter('Final Weekly Density 21-27.5.xlsx', engine='xlsxwriter')
df_new.to_excel(writer, sheet_name="Final Data", index=False)
pivot_table.to_excel(writer, sheet_name="Pivot table")
writer.close()



# # print("\n", df_new.shape)
#print(df_new.head())
# # print("")
#print(df_new.columns.values)

