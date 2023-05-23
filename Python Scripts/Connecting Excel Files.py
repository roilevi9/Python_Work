import os
import pandas as pd

def extract_lines_from_excel(main_folder_path, start_line):
    df = []
    for root, dirs, files in os.walk(main_folder_path):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                print('Loading file {0}...'.format(file))
                df.append(pd.read_excel(os.path.join(root, file), header=start_line-1))
    df_output = pd.concat(df, axis=0)
    df_output.to_excel("C:\\Users\\roil\\Documents\\OCC\\Output.xlsx", index=False)

print(extract_lines_from_excel("C:\\Users\\roil\\Documents\\OCC", 6))
