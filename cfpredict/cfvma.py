#!/usr/bin/env python

from .cfpredict import cfpredict

class cfvma(cfpredict):
    
    
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