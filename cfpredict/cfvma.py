#!/usr/bin/env python

from .cfpredict import cfpredict
import numpy as np
import pandas as pd

class cfvma(cfpredict):
    
    '''
    The sub class of the predictor of the commodity futures, with
    the strayegy of VMA and the properties of
    
    
    Attributes:
        length: the length of the time series data
    	is_data_loaded: the flag of boolean type to mark if the data is loaded
    	ts: the time series with the type of pandas dataframe
    
    Methods:
    	VMA: compute the VMA series of the time series by the return time n
    	    
    	    n: return time interval
    	    ts: time series to be computed
    	    vol: volume of the trade, to be the weight
    	    
    	double_VMA_curve: return the data of the double VMA of the specific dara term
    	
    	    Arguments:
    	    predict_time: the time interval of the return rate, default by 5
    	    start:  the start time, default by 0
    	    end: the end time, default by -1
    	    step: the sampling interval, default by 1
    	    short_term: the short term of the short VMA
    	    long_term: the long term of the long VMA
    	    label: the data term of the OLHC price data, can be
    
    	            'open': open price
    	            'low': lowest price
    	            'high': highest price
    	            'close': close price
    	            
    	    Return:
    	    vma_s: short VMA
    	    vma_l: long VMA
    	            
    	        
    	return_ratio_distribution_curve: return the data of the return rate of the specific data term
    	    Arguments:
    	    predict_time: the time interval of the return rate, default by 5
    	    short_term: the short term of the short VMA
    	    long_term: the long term of the long VMA
    	    label: the data term of the OLHC price data, can be
    	
    	    Return:
    	    f: index of the feature 1-l/s
            ratio: return rate
            f_gc: index of the feature where golden cross occurs
            r_gc: return rate where golden cross occurs
            f_dc: index of the feature where dead cross occurs
            r_dc: return rate where dead cross occurs
    
    	predict: method to predict the return rate, haing no idea how to do it for now
       
    '''
        
    def set_param(self, short_term, long_term):
        self.s = short_term
        self.l = long_term
        
        price = self.ts['close'][self.start:self.end:self.step]
        volume = self.ts['vol'][self.start:self.end:self.step]
        self.vma_s = self.VMA(self.s, price, volume)
        self.vma_l = self.VMA(self.l, price, volume)
    
    def VMA(self, n, ts, vol):
        vma = [0.0]*len(ts)
        for i in range(n, len(ts)):
            w = vol[i+1-n:i+1]
            vma[i] = np.dot(w, ts[i+1-n:i+1])/np.sum(w)
        return vma
    
    def double_VMA_curve(self, label='mean'):
        
        assert self.is_data_loaded == True, "Data hasn't been loaded yet! Try to use .load_data method to load the data"
        
        price = self.ts[label][self.start:self.end:self.step]
        volume = self.ts['vol'][self.start:self.end:self.step]
        vma_s = self.VMA(self.s, price, volume)
        vma_l = self.VMA(self.l, price, volume)
        
        return vma_s[self.l:len(volume)], vma_l[self.l:len(volume)]
    
    def return_ratio_distribution_curve(self, predict_time=5, label='mean'):
        
        s, l = self.double_VMA_curve(label)
        
        ratio = self.return_rate_curve(predict_time, label)[0:len(s)]
        
        f = [0.0]*len(s)
        for i in range(self.l, len(f)):
            f[i] = (l[i]-s[i])/(1.0*s[i])

        f_gc = []
        r_gc = []

        f_dc = []
        r_dc = []

        for i in range(self.l+1, len(f)-1):
            if s[i+1] > l[i+1] and s[i-1] < l[i-1] and s[i+1] > s[i-1]:
                f_gc.append(f[i])
                r_gc.append(ratio[i])
            elif s[i+1] < l[i+1] and s[i-1] > l[i-1] and s[i+1] < s[i-1]:
                f_dc.append(f[i])
                r_dc.append(ratio[i])
        
        return f, ratio, f_gc, r_gc, f_dc, r_dc
    
    
    
    def get_trade_signal(self, t):
        
        '''
        short selling signal for positive value and bull position signal for negative value 
        '''
        
        if t == 0:
            return 0
        elif self.vma_s[t-1] > self.vma_l[t-1] and self.vma_s[t] < self.vma_l[t]: # dead cross
            return 1
        elif self.vma_s[t-1] < self.vma_l[t-1] and self.vma_s[t] > self.vma_l[t]: # golden cross
            return -1
        else:
            return 0
    