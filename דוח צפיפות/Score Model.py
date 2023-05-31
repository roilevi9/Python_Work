import pandas as pd
import numpy as np

# Create DataFrame for table 1
df1 = pd.read_excel("Density Methodology.xlsx")

# Create DataFrame for table 2
df2 = pd.read_excel("C:\\Users\\roil\\Documents\\דוח צפיפות\\מאי 2023\\Final Weekly Density 21-27.5.xlsx")

# Merge the two tables based on the 'Time Range' column
merged_df = pd.merge(df2, df1, on='Time Range')


# Function to calculate scores based on the conditions
def calculate_score(row):
    if row['Number Of Passengers'] <= row['LNL']:
        return 100
    elif row['Number Of Passengers'] >= row['UNL']:
        return 0
    else:
        # Calculate relative score between the limits
        relative_range = row['UNL'] - row['LNL']
        relative_value = row['Number Of Passengers'] - row['LNL']
        relative_score = (relative_value / relative_range) * 100
        return relative_score


# Apply the calculate_score function to create the 'score' column
merged_df['Score'] = merged_df.apply(calculate_score, axis=1)
merged_df['Score'] = np.ceil(merged_df[['Score']]).astype(int)

# Display the resulting DataFrame
print(merged_df)
merged_df.to_excel("FINAL SCORE.xlsx", index=False)
