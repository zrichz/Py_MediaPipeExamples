#get covid data and plot deaths per country
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
import matplotlib.ticker as mtick

df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df = df[df['location'].isin(['United Kingdom', 'Germany', 'France', 'Italy', 'Spain'])]
df = df.loc[:,['date', 'location', 'total_deaths']]
df = df.pivot(index='date', columns='location', values='total_deaths')
df = df.fillna(method='ffill')
df = df.fillna(0)
df.plot(figsize=(10, 10), title='Total covid deaths per country')
plt.show()