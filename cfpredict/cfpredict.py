#!/usr/bin/env python
import numpy as np
import pandas as pd


class cfpredict:
    '''
    The base class of the predictor of the commodity futures, with
    the properties of
    
    
    Attributes:
        length: the length of the time series data
    	is_data_loaded: the flag of boolean type to mark if the data is loaded
    	ts: the time series with the type of pandas dataframe
        start: the start time index of the time series data to be processed
        end: the end time index of the time series data to be processed
        step: the sampling frequency of the time series data to be processed
    
    Methods:
    	load_data: take the dataframe of the time series as the argument
    	clear_data: clear the time series so you can decrease the size of the object
        sampling: sampling the original time series data
    	return_rate_curve: return the data of the return rate of the specific data term
    	    
    	    predict_time: the time interval of the return rate, default by 5
    	    label: the data term of the OLHC price data, can be
    	    
    	        'open': open price
    	        'low': lowest price
    	        'high': highest price
    	        'close': close price
    	
    	get_trade_signal: return the position to sell
        get_rate_of_return_curve: return the RR curve time series
    
    '''
    
    def __init__(self):
        self.length = 0
        self.is_data_loaded = False
        self.start = 0
        self.step = 1
    
    def load_data(self, df_ts):
        
        self.length = df_ts.shape[0]
        self.ts = df_ts
        self.is_data_loaded = True
        self.end = self.length
        
    def sampling(self, step, start=0, end=-1):
        self.start = start
        self.end = end
        self.step = step
        
    def clear_data(self):
        self.length = 0
        self.data = 0
        self.is_data_loaded = False
        self.start = 0
        self.end = -1
        self.step = 1
        
    def return_rate_curve(self, predict_time=5, label='mean'):
        
        assert self.is_data_loaded == True, "Data hasn't been loaded yet! Try to use .load_data method to load the data"
        
        ts_sampled = np.array(self.ts[label][self.start:self.end:self.step])
        r = np.array([0.0]*(len(ts_sampled)-predict_time))
        
        for i in range(len(r)):
            r[i] = 1.0*(ts_sampled[i+predict_time]-ts_sampled[i])/ts_sampled[i]
            
        return r
    
    def get_trade_signal(self, t): 
        
        '''
        short selling signal for positive value and bull position signal for negative value 
        '''
        
        return 0
    
    def get_rate_of_return_curve(self):
        
        assert self.is_data_loaded == True, "Data hasn't been loaded yet! Try to use .load_data method to load the data"
        
        capital = 0
        position = 1
    
        RR = [0.0]*len(self.ts['close'][self.start:self.end:self.step])
        trade = [0.0]*len(RR)        
        for i in range(len(RR)):
            
            s = self.get_trade_signal(i)  # short selling
            position -= s
            capital += s * self.ts['close'][i]
            
            RR[i] = 1.0*(capital + position * self.ts['close'][i])/self.ts['close'][self.start]
            trade[i] = s
            
        return RR, trade
    