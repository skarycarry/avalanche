import numpy as np
import pandas as pd
import statsmodels.api as sm

class ARIMAModel:
    def __init__(self, p, d, q):
        self.p = p
        self.d = d
        self.q = q
        self.model = None
        
    def fit(self, data):
        # Interpolate missing data points
        data_interpolated = data.interpolate(method='linear')
        
        # Fit ARIMA model to interpolated data
        self.model = sm.tsa.ARIMA(data_interpolated, order=(self.p, self.d, self.q)).fit()
        
    def predict(self, start, end):
        return self.model.predict(start=start, end=end, dynamic=False)

