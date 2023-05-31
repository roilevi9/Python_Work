import pandas as pd
import numpy as np

df = pd.read_excel("New All Records.xlsx")

Avg_Num_Of_Pass = round(df['Number Of Passengers'].mean())
Standard_deviation_Num_Of_Pass = round(df['Number Of Passengers'].std())

UNL = round(Avg_Num_Of_Pass + 3 * Standard_deviation_Num_Of_Pass)
LNL = round(Avg_Num_Of_Pass - 3 * Standard_deviation_Num_Of_Pass)

print("The AVG is: ", Avg_Num_Of_Pass, '\n')
print("The STD is: ", Standard_deviation_Num_Of_Pass, '\n')
print("The UNL is: ", UNL, '\n')
print("The LNL is: ", LNL, '\n')

AVG_pivot_table = pd.pivot_table(df, values="Number Of Passengers", index='Time Range', aggfunc=np.mean, fill_value=0)
print(AVG_pivot_table)
STD_pivot_table = pd.pivot_table(df, values="Number Of Passengers", index='Time Range', aggfunc=np.std, fill_value=0)
print(STD_pivot_table, "\n")

limits_table = pd.merge(AVG_pivot_table, STD_pivot_table, on='Time Range')
limits_table = limits_table.reset_index()
print(limits_table, "\n")

column_names = ['Time Range', 'Avg_Num_Of_Pass', 'STD_Num_Of_Pass']
limits_table.columns = column_names
print(limits_table, "\n")

limits_table['UNL'] = limits_table['Avg_Num_Of_Pass'] + 3 * limits_table['STD_Num_Of_Pass']
limits_table['LNL'] = limits_table['Avg_Num_Of_Pass'] - 3 * limits_table['STD_Num_Of_Pass']
limits_table["LNL"] = limits_table["LNL"].apply(lambda x: 112 if x < 112 else x)
limits_table[['Avg_Num_Of_Pass', 'STD_Num_Of_Pass', 'UNL', "LNL"]] = np.ceil(limits_table[['Avg_Num_Of_Pass', 'STD_Num_Of_Pass', 'UNL', "LNL"]]).astype(int)
print(limits_table, "\n")


limits_table.to_excel("Density Methodology.xlsx", index=False)
