import pandas as pd

df = pd.read_csv("data/raw_weather.csv")

print(df.head())
print(df.info())
print(df.describe())
df['date'] = pd.to_datetime(df['date'])
df = df[['date', 'temp', 'rainfall', 'humidity']]
df = df.fillna({
    'temp': df['temp'].mean(),
    'humidity': df['humidity'].mean(),
    'rainfall': 0
})
import numpy as np

daily_mean = np.mean(df['temp'])
daily_std = np.std(df['temp'])

df['month'] = df['date'].dt.month
monthly_stats = df.groupby('month')['temp'].agg(['mean', 'min', 'max', 'std'])
plt.plot(df['date'], df['temp'])
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Daily Temperature Trend")
plt.savefig("images/daily_temperature.png")
monthly_rain = df.groupby('month')['rainfall'].sum()
plt.bar(monthly_rain.index, monthly_rain.values)
plt.savefig("images/monthly_rainfall.png")
plt.scatter(df['temp'], df['humidity'])
plt.savefig("images/humidity_vs_temp.png")
fig, ax = plt.subplots(1, 2, figsize=(12,5))

ax[0].plot(df['date'], df['temp'])
ax[1].scatter(df['temp'], df['humidity'])
plt.savefig("images/combined_plots.png")
monthly = df.groupby(df['date'].dt.month).agg({
    'temp': 'mean',
    'rainfall': 'sum',
    'humidity': 'mean'
})
def season(month):
    if month in [12,1,2]: return "Winter"
    if month in [3,4,5]: return "Summer"
    if month in [6,7,8]: return "Monsoon"
    return "Autumn"

df['season'] = df['month'].apply(season)
seasonal = df.groupby('season').mean()
df.to_csv("data/cleaned_weather.csv", index=False)