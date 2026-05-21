import pandas as pd

print("==== CSV FILE ====")
try:
    df1 = pd.read_csv('powerdemand_5min_2021_to_2024_with weather.csv', nrows=3)
    print("Columns: ", list(df1.columns))
    print(df1.head(2))
except Exception as e:
    print("CSV Error:", e)

print("\n==== HOURLY LOAD INDIA ====")
try:
    df2 = pd.read_excel('hourlyLoadDataIndia.xlsx', nrows=3)
    print("Columns: ", list(df2.columns))
    print(df2.head(2))
except Exception as e:
    print("Excel Error:", e)

print("\n==== MONTHLY TEMP ====")
try:
    df3 = pd.read_excel('monthly_temp.xlsx', nrows=3)
    print("Columns: ", list(df3.columns))
    print(df3.head(2))
except Exception as e:
    print("Excel Error:", e)
