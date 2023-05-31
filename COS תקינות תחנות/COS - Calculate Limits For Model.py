import pandas as pd
from scipy import stats

df = pd.read_excel("COS - All Deviations.xlsx", parse_dates=["Date"])
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

df.drop(['Status', 'Status comments', "Location", "Name of employee", "Amount", "Location at end", 'Does appear in TJ reports'], axis=1, inplace=True)
print(df.columns)

df.dropna(subset=['Fault'], how='all', inplace=True)
df.reset_index(drop=True)

df['PS'] = df['Name of station'] + " / " + df['Platform']
df['Amount_DEV'] = 1 + df['Fault'].str.count(',')
df['MonthYear'] = df['Date'].dt.strftime('%Y-%m')
print(df.head(), '\n')

pivot_table = pd.pivot_table(df, values='Amount_DEV', index='MonthYear', aggfunc='sum')
print(pivot_table, "\n")
MIN_DEV = df["Amount_DEV"].min()
print("MIN: ", MIN_DEV, '\n')
MAX_DEV = df["Amount_DEV"].max()
print("MAX: ", MAX_DEV, '\n')
AVG_DEV = df["Amount_DEV"].mean()
print("AVG: ", AVG_DEV, '\n')
STD_DEV = df["Amount_DEV"].std()
print("STD: ", STD_DEV, '\n')


values_to_drop = ["2022-08", "2022-09", "2022-10"]

# Filter the DataFrame to exclude rows with values in the "A" column matching the array
filtered_data = df[~df['MonthYear'].isin(values_to_drop)]

pivot_table2 = pd.pivot_table(filtered_data, values='Amount_DEV', index='MonthYear', aggfunc='sum')
print(pivot_table2, "\n")

MIN_DEV_F = filtered_data["Amount_DEV"].min()
print("MIN: ", MIN_DEV_F, '\n')
MAX_DEV_F = filtered_data["Amount_DEV"].max()
print("MAX: ", MAX_DEV_F, '\n')
AVG_DEV_F = filtered_data["Amount_DEV"].mean()
print("AVG: ", AVG_DEV_F, '\n')
STD_DEV_F = filtered_data["Amount_DEV"].std()
print("STD: ", STD_DEV_F, '\n')

pivot_table3 = pivot_table2.reset_index()
print(pivot_table3, "\n")
MIN_DEV_P = pivot_table3["Amount_DEV"].min()
print("MIN: ", MIN_DEV_P, '\n')
MAX_DEV_P = pivot_table3["Amount_DEV"].max()
print("MAX: ", MAX_DEV_P, '\n')
AVG_DEV_P = pivot_table3["Amount_DEV"].mean()
print("AVG: ", AVG_DEV_P, '\n')
STD_DEV_P = pivot_table3["Amount_DEV"].std()
print("STD: ", STD_DEV_P, '\n')

UNL = round(AVG_DEV_P + 3 * STD_DEV_P)

if (AVG_DEV_P - 3 * STD_DEV_P) < 0:
    LNL = 0
else:
    LNL = round(AVG_DEV_P - 3 * STD_DEV_P)

print("The UNL is: ", UNL, '\n')
print("The LNL is: ", LNL, '\n')


# Calculate the average number of failures per day for each station
# avg_failures = df.groupby('PS')['Amount_DEV'].mean().reset_index()
#
# # Determine the grading bins dynamically
# num_bins = 3  # Number of grading bins
# labels = ['low', 'medium', 'high']  # Grade labels
#
# avg_failures['Grade'] = pd.qcut(avg_failures['Amount_DEV'], num_bins, labels=labels)
# print(avg_failures)
# Merge the grades DataFrame with the original data
# merged_data = pd.merge(df, avg_failures[['PS', 'Grade']], on='Station', how='left')



