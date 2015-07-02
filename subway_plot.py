# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:00:11 2015

@author: Stefan
"""

import numpy as np
from pandas import *
from ggplot import *



if __name__ == "__main__":
 
    data = pandas.read_csv('turnstile_weather_v2.csv')
    # select some features
    features = data[['station', 'day_week', 'ENTRIESn_hourly']]
    # convert date to weekday
    # group, average for weekday and get dataframe
    grouped = DataFrame(np.around(features.groupby(['day_week', 'station']).mean())).reset_index()
    # scale and set threshold, no threshold
    cut = grouped[grouped.ENTRIESn_hourly > -1]
    # flatten ridership  log base 1.5
    cut.ENTRIESn_hourly = np.exp(np.log(cut.ENTRIESn_hourly) / 1.5)
    # replace unit names by continouos number
    unit_names, unit_place = np.unique(cut.station, return_index = True) 
    unq_units = DataFrame({'place': np.add(unit_place, 1), 'name': unit_names})
    cut.station = cut.station.astype('category').cat.rename_categories(unq_units.place)  
    
    print ggplot(cut, aes(y='station', x='day_week', color='ENTRIESn_hourly')) + \
    geom_point(size=10, alpha=0.8) + \
    scale_colour_gradient(low='white', high='red') + \
    labs(title = 'Ridership by Day of Week and Station (logarithmic)', x='Day of Week', y='Station Id') + \
    ylim(-25, 225) + xlim(-.5, 6.5) + theme_bw()

  
   