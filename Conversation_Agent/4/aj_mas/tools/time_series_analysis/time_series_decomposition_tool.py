from ..base_tool import BaseTool
from utils.logger import logger
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import matplotlib.pyplot as plt

class TimeSeriesDecompositionTool(BaseTool):
    def __init__(self):
        super().__init__("Time Series Decomposition", "Decompose time series into trend, seasonal, and residual components")

    def execute(self, data: pd.Series, period: int, model: str = 'additive'):
        logger.log(f"Executing Time Series Decomposition Tool")
        try:
            result = seasonal_decompose(data, model=model, period=period)
            
            plt.figure(figsize=(12, 10))
            plt.subplot(411)
            plt.plot(result.observed)
            plt.title('Observed')
            plt.subplot(412)
            plt.plot(result.trend)
            plt.title('Trend')
            plt.subplot(413)
            plt.plot(result.seasonal)
            plt.title('Seasonal')
            plt.subplot(414)
            plt.plot(result.resid)
            plt.title('Residual')
            plt.tight_layout()
            plt.savefig('time_series_decomposition.png')
            plt.close()

            return {
                'trend': result.trend.to_dict(),
                'seasonal': result.seasonal.to_dict(),
                'residual': result.resid.to_dict(),
                'plot': 'time_series_decomposition.png'
            }
        except Exception as e:
            return f"Error in time series decomposition: {str(e)}"