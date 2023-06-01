import pandas as pd
from scipy import stats


df = pd.read_excel("New All Records.xlsx")
data = df["Number Of Passengers"]

result = stats.anderson(data)
statistic = result.statistic
critical_values = result.critical_values
significance_levels = result.significance_level

print(f"Statistic: {statistic}")

for i, alpha in enumerate(significance_levels):
    if statistic < critical_values[i]:
        print(f"Data appears to be normally distributed at the {alpha}% significance level.")
    else:
        print(f"Data does not appear to be normally distributed at the {alpha}% significance level.")
