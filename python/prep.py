import numpy as np
import pandas as pd
from plotnine import *

# load data files 
reference_pt = pd.read_csv("../data/portugal_monthly_avg.csv", \
                           header = None, \
                           names = ['reference'])
temperature_pt = pd.read_csv("../data/portugal_monthly_anom.csv", \
                             header = None, \
                             names = ['year', 'month', 'delta'])
reference_world = pd.read_csv("../data/world_monthly_avg.csv", \
                              header = None, \
                              names = ['reference'])
temperature_world = pd.read_csv("../data/world_monthly_anom.csv", \
                  header = None, \
                  names = ['year', 'month', 'delta'])

reference_pt['month'] = range(1, 13)
reference_world['month'] = range(1, 13)

# --- calculate temperatures from reference and delta temperature files

def calculate_temperatures(ref_temp, delta_temp, loc):
        assert 'delta' in delta_temp.columns, 'delta_temp lacks a delta column'
        assert 'reference' in ref_temp.columns, 'ref_temp lacks a reference column'
        temp = ref_temp.merge(delta_temp, on = 'month')
        temp['absolute'] = temp.reference + temp.delta
        # remove years with missing measurements
        temp['count'] = temp.groupby('year')['year'].transform('count')
        temp = temp.query('count == 12')
        # average annual temperature
        temp = temp.groupby('year').mean()[['absolute']]
        temp['year'] = temp.index
        assert temp.year.duplicated().sum() == 0, "remove duplicate years"
        temp['location'] = np.repeat(loc, len(temp))
        return temp

temperature_pt = calculate_temperatures(reference_pt, temperature_pt, "Portugal")
temperature_world = calculate_temperatures(reference_world, temperature_world, "World")

# --- combine data frames

temperatures = pd.concat([temperature_pt, temperature_world], ignore_index = True)
temperatures = temperatures.dropna()

# ------- line charts with moving averages

p = ggplot(temperatures, aes(x = 'year', y = 'absolute', color = 'location')) \
  + geom_point(alpha = .4, size = 2) \
  + geom_smooth(method = "mavg", method_args = {'window': 10},  se = False) \
  + labs(x = 'Year', y = 'Average Temperature') \
  + theme_minimal() \
  + theme(legend_position = (0.75, 0.25))
