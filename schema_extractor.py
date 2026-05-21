import pandas as pd
import json

out = {}
try:
    df1 = pd.read_csv('powerdemand_5min_2021_to_2024_with weather.csv', nrows=2)
    out['powerdemand'] = dict(zip(df1.columns, [str(x) for x in df1.dtypes]))
except Exception as e: out['powerdemand'] = str(e)

try:
    df2 = pd.read_excel('hourlyLoadDataIndia.xlsx', nrows=2)
    out['hourlyLoad'] = dict(zip(df2.columns, [str(x) for x in df2.dtypes]))
except Exception as e: out['hourlyLoad'] = str(e)

try:
    df3 = pd.read_excel('monthly_temp.xlsx', nrows=2)
    out['monthlyTemp'] = dict(zip(df3.columns, [str(x) for x in df3.dtypes]))
except Exception as e: out['monthlyTemp'] = str(e)

with open('schema.json', 'w') as f:
    json.dump(out, f, indent=2)
