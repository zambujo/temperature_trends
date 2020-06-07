import numpy as np
import pandas as pd
from plotnine import *

# load data files 
base_local=pd.read_csv("../data/portugal_monthly_avg.csv",\
                       header=None,\
                       names=['baseline'])
local=pd.read_csv("../data/portugal_monthly_anom.csv", \
                  header=None, \
                  names=['year', 'month', 'anomaly'])
base_world=pd.read_csv("../data/world_monthly_avg.csv",\
                        header=None,\
                        names=['baseline'])
world=pd.read_csv("../data/world_monthly_anom.csv", \
                  header=None, \
                  names=['year', 'month', 'anomaly'])

base_local['month']=range(1, 13)
base_world['month']=range(1, 13)

# --- calculate temperatures from baselines and anomalies

local=pd.merge(local, base_local, on='month', how='left')
local['temp']=local.baseline + local.anomaly
local['count']=local.groupby('year')['year'].transform('count')
local=local.query('count == 12')
local=local.groupby('year').mean()[['temp']]
local['year']=local.index
local['location']=np.repeat("Portugal", len(local))
assert local.year.duplicated().sum() == 0, \
       "TODO: remove duplicates from local dataframe"

world=pd.merge(world, base_world, on='month', how='left')
world['temp']=world.baseline + world.anomaly
world['count']=world.groupby('year')['year'].transform('count')
world=world.query('count == 12')
world=world.groupby('year').mean()[['temp']]
world['year']=world.index
world['location']=np.repeat("World", len(world))
assert world.year.duplicated().sum() == 0, \
       "TODO: remove duplicates from world data frame"

# --- combine data frames

tt=pd.concat([local, world], ignore_index=True)
tt=tt.dropna()

# ------- line charts with moving averages

p=ggplot(tt, aes(x='year', y = 'temp', color = 'location')) \
+ geom_point(alpha = .4, size = 2) \
+ geom_smooth(method = "mavg", method_args={'window': 10},  se=False) \
+ labs(x = 'Year', y = 'Average Temperature') \
+ theme_minimal() \
+ theme(legend_position = (0.75, 0.25))
