import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

print("Applying ETL pipeline to real Kaggle dataset...")
df = pd.read_csv('powerdemand_5min_2021_to_2024_with weather.csv')

print("Raw data loaded. Shape:", df.shape)

# Create Block numbers from hour and minute
# Block 1 is 00:00 to 00:15
df['block'] = (df['hour'] * 4) + (df['minute'] // 15) + 1

# Aggregate 5-minute data into 15-minute market blocks
print("Aggregating 5-minute data into 15-minute market blocks...")
grouped = df.groupby(['year', 'month', 'day', 'block']).agg({
    'Power demand': 'mean',
    'temp': 'mean',
    'rhum': 'mean',
    'wspd': 'mean'
}).reset_index()

grouped = grouped.dropna()

print("Engineered Block-level Data Shape:", grouped.shape)

# We must mathematically simulate historical Price Discovery since the dataset only provides Demand/Weather
print("Simulating historical MCP (Market Clearing Prices)...")
demand = grouped['Power demand']
temp = grouped['temp']

# Real prices naturally trend up intensely with high demand and extreme temps
price = 2.0 + (demand / demand.mean()) * 3.0 + (temp / 35.0) * 1.5 + np.random.normal(0, 0.5, len(grouped))
price = np.maximum(price, 1.0) # Market price floor is usually above 0
grouped['price'] = price

print("Training Scikit-Learn Model on Kaggle Dataset...")
# Features selected: block, month, temp, rhum, wspd, Power demand
X = grouped[['block', 'month', 'temp', 'rhum', 'wspd', 'Power demand']]
y = grouped['price']

model = RandomForestRegressor(n_estimators=30, max_depth=12, random_state=42, n_jobs=-1)
model.fit(X, y)

os.makedirs('models', exist_ok=True)
model_path = os.path.join('models', 'rf_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Kaggle Model successfully trained and saved to {model_path}!")
