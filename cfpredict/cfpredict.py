#!/usr/bin/env python

import pandas as pd
import numpy as np

class cfpredict:
    """
    The base class of the predictor of the commodity futures, with
    the properties of
    
    
    Attributes:
        length: the length of the time series data
    	is_data_loaded: the flag of boolean type to mark if the data is loaded
    	ts: the time series with the type of pandas dataframe
    
    Methods:
    	load_data: take the dataframe of the time series as the argument
    	clear_data: clear the time series so you can decrease the size of the object
    	return_rate_curve: return the data of the return rate of the specific data term
    	    
    	    predict_time: the time interval of the return rate, default by 5
    	    start:  the start time, default by 0
    	    end: the end time, default by -1
    	    step: the sampling interval, default by 1
    	    label: the data term of the OLHC price data, can be
    	    
    	        'open': open price
    	        'low': lowest price
    	        'high': highest price
    	        'close': close price
    	
    	predict: method to predict the return rate, haing no idea how to do it for now
    
    """ 
    
    def __init__(self):
        self.length = 0
        self.is_data_loaded = False
    
    def load_data(self, df_ts):
        
        self.length = df_ts.shape[0]
        self.ts = df_ts
        self.is_data_loaded = True
        
    def clear_data(self):
        self.length = 0
        self.data = 0
        self.is_data_loaded = False
        
    def return_rate_curve(self, predict_time=5, start=0, end=-1, step=1, label='mean'):
        
        assert self.is_data_loaded == True, "Data hasn't been loaded yet! Try to use .load_data method to load the data"
        
        if end == -1:
            end = self.length
        
        ts_sampled = np.array(self.ts[label][start:end:step])
        r = np.array([0.0]*(len(ts_sampled)-predict_time))
        
        for i in range(len(r)):
            r[i] = 1.0*(ts_sampled[i+predict_time]-ts_sampled[i])/ts_sampled[i]
            
        return r
    
    def predict():
        
        return 0
        
