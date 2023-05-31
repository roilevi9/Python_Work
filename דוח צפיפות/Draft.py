import pandas as pd
import numpy as np

df = pd.read_excel("All Records - Cfir - First Sorting 3.xlsx")

Seats_Per_Car = 56
Standing = 34.5314
dev = 2.75

df.loc[df['Leading Trailer'] >= 46, 'Leading Trailer'] = np.nan
df.dropna(subset=['Leading Trailer'], how='all', inplace=True)
df['Section'] = df['Section'].apply(lambda x: '(' + '0' + x[x.find('(')+1:x.find(')')] + ')' + x[x.find(')')+1:] if isinstance(x, str) and len(x[x.find('(')+1:x.find(')')]) == 1 else x)
df.dropna(subset=['Section'], how='all', inplace=True)
df['Section'] = df['Section'].str[5:]

df['Date'] = df['Date'].str.replace('.', '/')
# df["T1"] = np.where((df["Model First Car"]-Seats_Per_Car) > 0, (df["Model First Car"]-Seats_Per_Car)/Standing, 0)
# df["T2"] = np.where((df["Model Second Car"]-Seats_Per_Car) > 0, (df["Model Second Car"]-Seats_Per_Car)/Standing, 0)
# df["DEV"] = np.where((df["T1"] > dev) | (df["T2"] > dev), 1, 0)



writer = pd.ExcelWriter('New All Records.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name="New All Records", index=False)
writer.close()
