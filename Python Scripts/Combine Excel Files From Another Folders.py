import os
import pandas as pd
import numpy as np

main_folder_path = "C:\\Users\\roil\\Documents\\OCC"
start_line = 6
df = []
for root, dirs, files in os.walk(main_folder_path):
    for file in files:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            print('Loading file {0}...'.format(file))
            df.append(pd.read_excel(os.path.join(root, file), header=start_line-1))
df_output = pd.concat(df, axis=0)

print(df_output.head())
column_names = ['Event Number', 'Event start date', 'Event end date', 'Train / WP', 'Running Board', 'Area', 'Track Number', 'Service code', 'Service Code Description',
                'Caller operation description', 'Road / Equipment', 'Equipment description', 'Employee reports', 'Operator name', 'Assigned for', 'Date of registration in the system',
                'Event Description', 'Comments 1', 'Comments 2']
df_output.columns = column_names

df_output['Event start date'] = pd.to_datetime(df_output['Event start date'], errors='coerce')
df_output = df_output.dropna(subset=['Event start date'])
df_output = df_output.reset_index(drop=True)

# # specific_date = pd.to_datetime("01-03-2022")
# # df_filtered = df_output[df_output["Event start date"] >= specific_date]
# # df_filtered = df_filtered.reset_index(drop=True)


Safety_Array = ["Spad", "SPAD", "accident", "Accident", "emergency", "Emergency", "Brake", "Braking", "brake", "braking"]
Depot_Array = ['Depot', 'depot', 'DEPOT', 'DPT', 'dpt', 'Dpt', 'DPFH', 'Dpfh', 'DPfh']


# Define a function to check if any of the expressions are in a given cell
def safety_contains_expression(cell_value):
    if isinstance(cell_value, float):
        cell_value = str(cell_value)
    return any(expression in cell_value for expression in Safety_Array)


def depot_expression(cell_value):
    if isinstance(cell_value, float):
        cell_value = str(cell_value)
    return any(expression in cell_value for expression in Depot_Array)


df_output['Safety'] = df_output['Service Code Description'].apply(safety_contains_expression).astype(int)
df_output['Depot'] = df_output['Area'].apply(depot_expression).astype(int)
df_output = df_output[df_output['Depot'] != 1]
df_output = df_output[df_output['Safety'] != 0]
df_output = df_output.drop('Depot', axis=1)
df_ascending = df_output.sort_values(by='Event start date', ascending=True)

# Monthly analysis:
Safety_Pivot = pd.pivot_table(df_ascending, values="Safety", index=pd.Grouper(key='Event start date', freq="M"), aggfunc=np.sum, fill_value=0)
pivot_table = Safety_Pivot.reset_index()
pivot_table['Year'] = pivot_table['Event start date'].dt.year
annual_stats = pivot_table.groupby('Year')['Safety'].agg(['sum', 'min', 'max', 'mean', 'std'])
column_names = ['Total Safety Dev Per Year', 'Min Safety Dev For Year', 'Max Safety Dev For Year', 'Avg Safety Dev For Year', 'STD For Year']
annual_stats.columns = column_names
print(annual_stats)

values_array = Safety_Pivot.iloc[:, 0].values
date_array = np.array(Safety_Pivot.index.values)
dates = pd.to_datetime(date_array)
month_year_array = [(str(date.month) + "-" + str(date.year)) for date in dates]
month_year_Dev = pd.DataFrame(index=month_year_array, data=values_array, columns=["Total Safety Dev Per Month"])
print(Safety_Pivot, '\n')
print(month_year_Dev, '\n')


writer = pd.ExcelWriter('C:\\Users\\roil\\Documents\\OCC\\Total Safety Records.xlsx', engine='xlsxwriter')
df_ascending.to_excel(writer, sheet_name="Safety Records", index=False)
month_year_Dev.to_excel(writer, sheet_name="Monthly Analysis")
annual_stats.to_excel(writer, sheet_name="Annual Analysis")
writer.close()

# df_output.to_excel("C:\\Users\\roil\\Documents\\OCC\\Output.xlsx", index=False)
#df_output.to_excel("C:\\Users\\roil\\Documents\\Output.xlsx", index=False)
