import pandas as pd

Safety_Array = ["Spad", "SPAD", "accident","Accident", "emergency","Emergency", "Brake", "Braking", "brake", "braking"]

df = pd.read_excel("FCC/OCC REPORTS - מרץ 2023.xlsx")
# Define a function to check if any of the expressions are in a given cell
def contains_expression(cell_value):
    return any(expression in cell_value for expression in Safety_Array)

# Create a new column in the DataFrame indicating whether each row contains any of the expressions
df['Safety'] = df['Service Code Description'].apply(contains_expression).astype(int)

df.to_excel('FCC/OCC Final Report March.xlsx', index=False)
