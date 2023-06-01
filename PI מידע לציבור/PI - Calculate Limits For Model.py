import pandas as pd

df = pd.read_excel("All records of Cfir - PI.xlsx")

# Convert the "Date" column to datetime format with a custom format string
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')


df.drop(['Status', 'Status comments', "location", "Name of employee", "Number of vehicle else", "Location at end of process", 'Does appear in TJ reports', 'Free comments', 'Ending time'], axis=1, inplace=True)
print(df.columns, "\n")

df['MonthYear'] = df['Date'].dt.strftime('%Y-%m')

pivot_table = pd.pivot_table(df, values='RecordID', index='MonthYear', aggfunc='count')
print(pivot_table, "\n")

pivot_table2 = pivot_table.reset_index()
pivot_table2.columns = ['Month Year', 'Count Of DEV']
print(pivot_table2, "\n")

MIN_DEV_P = pivot_table2["Count Of DEV"].min()
print("MIN: ", MIN_DEV_P, '\n')
MAX_DEV_P = pivot_table2["Count Of DEV"].max()
print("MAX: ", MAX_DEV_P, '\n')
AVG_DEV_P = pivot_table2["Count Of DEV"].mean()
print("AVG: ", AVG_DEV_P, '\n')
STD_DEV_P = pivot_table2["Count Of DEV"].std()
print("STD: ", STD_DEV_P, '\n')

UNL = round(AVG_DEV_P + 3 * STD_DEV_P)

if (AVG_DEV_P - 3 * STD_DEV_P) < 0:
    LNL = 0
else:
    LNL = round(AVG_DEV_P - 3 * STD_DEV_P)

print("The UNL is: ", UNL, '\n')
print("The LNL is: ", LNL, '\n')
