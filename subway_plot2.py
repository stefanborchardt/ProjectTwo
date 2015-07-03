# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:00:11 2015

@author: Stefan
"""

from pandas import *
from ggplot import *



if __name__ == "__main__":
 
    data = pandas.read_csv('turnstile_weather_v2.csv')
    # select some features
    features = data[['rain', 'hour', 'ENTRIESn_hourly']]
    # group, average by hour and get dataframe
    grouped = DataFrame(features.groupby(['rain', 'hour']).mean()).reset_index()
        
    print(ggplot(grouped, aes(x='hour', y='ENTRIESn_hourly', color='rain')) + \
    geom_line() + geom_point() + labs(title='Impact of Rain', \
    x='Time of Day', y='Ridership')) + xlim(0,20)
    
  
   