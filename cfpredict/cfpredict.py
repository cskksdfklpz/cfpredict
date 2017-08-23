#!/usr/bin/env python

class cfpredict:
    """
    The base class of the predictor of the commodity futures, with
    the properties of

    
        
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
        
