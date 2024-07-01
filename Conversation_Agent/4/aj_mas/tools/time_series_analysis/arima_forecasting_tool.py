from ..base_tool import BaseTool
from utils.logger import logger
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import matplotlib.pyplot as plt

class ARIMAForecastingTool(BaseTool):
    def __init__(self):
        super().__init__("ARIMA Forecasting", "Forecast time series data using ARIMA model")

    def execute(self, data: pd.Series, order: tuple, steps: int):
        logger.log(f"Executing ARIMA Forecasting Tool")
        try:
            model = ARIMA(data, order=order)
            results = model.fit()
            forecast = results.forecast(steps=steps)
            
            plt.figure(figsize=(10, 6))
            plt.plot(data.index, data, label='Observed')
            plt.plot(forecast.index, forecast, color='red', label='Forecast')
            plt.title('ARIMA Forecast')
            plt.legend()
            plt.savefig('arima_forecast.png')
            plt.close()

            return {
                'forecast': forecast.to_dict(),
                'plot': 'arima_forecast.png'
            }
        except Exception as e:
            return f"Error in ARIMA forecasting: {str(e)}"