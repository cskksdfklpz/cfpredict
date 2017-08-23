#!/usr/bin/env python

from .cfpredict import cfpredict

class cfvma(cfpredict):
    
    """
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
    	    start:  the start time, default by 0
    	    end: the end time, default by -1
    	    step: the sampling interval, default by 1
    	    short_term: the short term of the short VMA
    	    long_term: the long term of the long VMA
    	    label: the data term of the OLHC price data, can be
    	
    	    Return:
    	    
    
    	predict: method to predict the return rate, haing no idea how to do it for now
        f: index of the feature 1-l/s
        ratio: return rate
        f_gc: index of the feature where golden cross occurs
        r_gc: return rate where golden cross occurs
        f_dc: index of the feature where dead cross occurs
        r_dc: return rate where dead cross occurs
    """ 
    
    def VMA(self, n, ts, vol):
        vma = [0.0]*len(ts)
        for i in range(n, len(ts)):
            w = vol[i+1-n:i+1]
            vma[i] = np.dot(w, ts[i+1-n:i+1])/np.sum(w)
        return vma
    
    def double_VMA_curve(self, start=0, end=-1, step=1, short_term=12, long_term=26, label='mean'):
        
        assert self.is_data_loaded == True, "Data hasn't been loaded yet! Try to use .load_data method to load the data"
        
        if end == -1:
            end = self.length
        
        price = self.ts[label][start:end:step]
        volume = self.ts['vol'][start:end:step]
        vma_s = self.VMA(short_term, price, volume)
        vma_l = self.VMA(long_term, price, volume)
        
        return vma_s[long_term:len(volume)], vma_l[long_term:len(volume)]
    
    def return_ratio_distribution_curve(self, predict_time=5, start=0, end=-1, step=1, short_term=12, long_term=26, label='mean'):
        
        
        s, l = self.double_VMA_curve(start, end, step, short_term, long_term, label)
        
        ratio = self.return_rate_curve(predict_time, start, end, step, label)[0:len(s)]
        
        f = [0.0]*len(s)
        for i in range(long_term, len(f)):
            f[i] = (l[i]-s[i])/(1.0*s[i])

        f_gc = []
        r_gc = []

        f_dc = []
        r_dc = []

        for i in range(long_term+1, len(f)-1):
            if s[i+1] > l[i+1] and s[i-1] < l[i-1] and s[i+1] > s[i-1]:
                f_gc.append(f[i])
                r_gc.append(ratio[i])
            elif s[i+1] < l[i+1] and s[i-1] > l[i-1] and s[i+1] < s[i-1]:
                f_dc.append(f1[i])
                r_dc.append(ratio[i])
        
        return f, ratio, f_gc, r_gc, f_dc, r_dc