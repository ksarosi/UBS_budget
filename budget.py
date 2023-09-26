import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# Specify the path to your tab-delimited CSV file
csvpath_debit = os.path.join("export.csv")
csvpath_credit = os.path.join("transactions.csv")
csvpath_savings = os.path.join("export-2.csv")

# Read the tab-delimited CSV file
budget_df_debit = pd.read_csv(csvpath_debit, encoding='iso-8859-1', delimiter=';')
budget_df_credit = pd.read_csv(csvpath_credit, encoding='iso-8859-1', delimiter=';')
budget_df_credit = budget_df_credit.rename(columns={'Purchase date': 'Value date'})
budget_df_savings = pd.read_csv(csvpath_savings, encoding='iso-8859-1', delimiter=';')

budget_df_debit['Debit'] = budget_df_debit['Debit'].str.replace(",", "").str.replace("'", "").astype(float)
budget_df_debit['Credit'] = budget_df_debit['Credit'].str.replace(",", "").str.replace("'", "").astype(float)
budget_df_debit['Balance'] = budget_df_debit['Balance'].str.replace(",", "").str.replace("'", "").astype(float)

budget_df_savings['Debit'] = budget_df_savings['Debit'].str.replace(",", "").str.replace("'", "").astype(float)
budget_df_savings['Credit'] = budget_df_savings['Credit'].str.replace(",", "").str.replace("'", "").astype(float)
budget_df_savings['Balance'] = budget_df_savings['Balance'].str.replace(",", "").str.replace("'", "").astype(float)


merged_df = pd.concat([budget_df_credit, budget_df_debit, budget_df_savings], ignore_index=True)

budget_df = merged_df.set_index('Value date')
budget_df.index = pd.to_datetime(budget_df.index, dayfirst = True)
budget_df = budget_df.sort_index()

grouped_df = budget_df.groupby(budget_df.index).sum()
grouped_df['Total'] = np.nan
# Initialize the starting balance
starting_balance = 4129 + 4994.7 + 1296.57


# Calculate the cumulative balance based on transactions
for index, row in grouped_df.iterrows():
    if np.isfinite(row['Debit']):
        starting_balance -= row['Debit']
    if np.isfinite(row['Credit']):
        starting_balance += row['Credit']
    if np.isfinite(row['Individual amount']):
        starting_balance += row['Individual amount']
    grouped_df.at[index, 'Total'] = starting_balance



# Plot the time series data using row index as x-values
plt.figure(figsize=(12, 6))
plt.plot(grouped_df.index, grouped_df['Total'], label='Balance')
plt.xlabel('Entry Index')
plt.ylabel('Balance')
plt.title('Balance - Main account')
plt.legend()
plt.grid(True)


csvpath = os.path.join("export-2.csv")
# Read the tab-delimited CSV file
budget_df = pd.read_csv(csvpath, encoding='iso-8859-1', delimiter=';')
budget_df = budget_df.set_index('Value date')
budget_df.index = pd.to_datetime(budget_df.index, dayfirst = True)
budget_df = budget_df.sort_index()

starting_balance = 4994.7

# Create a 'Balance' column with NaN values
budget_df['Balance'] = np.nan
budget_df['Debit'] = budget_df['Debit'].str.replace(",", "").str.replace("'", "").astype(float)
budget_df['Credit'] = budget_df['Credit'].str.replace(",", "").str.replace("'", "").astype(float)

# Calculate the cumulative balance based on transactions
for index, row in budget_df.iterrows():
    if np.isfinite(row['Debit']):
        starting_balance -= row['Debit']
    elif np.isfinite(row['Credit']):
        starting_balance += row['Credit']
    elif np.isfinite(row['Individual amount']):
        starting_balance += row['Individual amount']
    budget_df.at[index, 'Balance'] = starting_balance

# Plot the time series data using row index as x-values
plt.figure(figsize=(12, 6))
plt.plot(budget_df.index, budget_df['Balance'], label='Balance')
plt.xlabel('Entry Index')
plt.ylabel('Balance')
plt.title('Balance - Savings account')
plt.legend()
plt.grid(True)

csvpath = os.path.join("transactions.csv")
# Read the tab-delimited CSV file
budget_df = pd.read_csv(csvpath, encoding='iso-8859-1', sep=';')
budget_df = budget_df.set_index('Purchase date')
budget_df.index = pd.to_datetime(budget_df.index, dayfirst = True)
budget_df = budget_df.sort_index()

starting_balance = 1296.57

# Create a 'Balance' column with NaN values
budget_df['Balance'] = np.nan

# Calculate the cumulative balance based on transactions
for index, row in budget_df.iterrows():
    if np.isfinite(row['Debit']):
        starting_balance -= row['Debit']
    elif np.isfinite(row['Credit']):
        starting_balance += row['Credit']
    budget_df.at[index, 'Balance'] = starting_balance

# Plot the time series data using row index as x-values
plt.figure(figsize=(12, 6))
plt.plot(budget_df.index, budget_df['Balance'], label='Balance')
plt.xlabel('Entry Index')
plt.ylabel('Balance')
plt.title('Balance - Credit card')
plt.legend()
plt.grid(True)

print(budget_df.groupby(budget_df.Sector).sum()['Debit'].sort_values())
# Show the plot
plt.show()
