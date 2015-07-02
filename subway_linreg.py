# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:00:11 2015

@author: Stefan
"""

import numpy as np
import pandas
import statsmodels.api as sm

def normalize_features(features):
    ''' 
    Returns the means and standard deviations of the given features, along with a normalized feature
    matrix.
    ''' 
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    ''' 
    Recovers the weights for a linear model given parameters that were fitted using
    normalized features. Takes the means and standard deviations of the original
    features, along with the intercept and parameters computed using the normalized
    features, and returns the intercept and parameters that correspond to the original
    features.
    ''' 
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """

    model = sm.OLS(values, features)
    results = model.fit()
    
    return results

if __name__ == "__main__":
    # Load in the data, obtain features and values
    data = pandas.read_csv('turnstile_weather_v2.csv')
    #data = data[(data.ENTRIESn_hourly > 50) & (data.ENTRIESn_hourly < 5000)]
    
    # select some features
    features = data[['hour', 'rain']]
    
    # normalize numerical features
    means, std_devs, norm_features = normalize_features(features)
    
    # add day of week to features using dummy variables
    dummy_wd = pandas.get_dummies(data['day_week'], prefix='day')
    del dummy_wd[dummy_wd.icol(0).name]
    norm_features = norm_features.join(dummy_wd)
    
    # Add stations to features using dummy variables
    dummy_units = pandas.get_dummies(data['station'], prefix='station')
    del dummy_units[dummy_units.icol(0).name]
    norm_features = norm_features.join(dummy_units)
    
    # add intercept
    norm_features = sm.add_constant(norm_features)

    values = data['ENTRIESn_hourly']

    results = linear_regression(norm_features, values)
    
    norm_intercept = results.params[0]
    norm_params = results.params[1:]
    
    recover_params(means, std_devs, norm_intercept, norm_params)
    
    print(results.summary())

