from ..base_tool import BaseTool
from utils.logger import logger
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

class RegressionTool(BaseTool):
    def __init__(self):
        super().__init__("Regression", "Perform linear regression on data")

    def execute(self, X: np.array, y: np.array):
        logger.log(f"Executing Regression Tool")
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            plt.figure(figsize=(10, 6))
            plt.scatter(X_test, y_test, color='blue', label='Actual')
            plt.plot(X_test, y_pred, color='red', label='Predicted')
            plt.title('Linear Regression')
            plt.legend()
            plt.savefig('regression_result.png')
            plt.close()

            return {
                'coefficients': model.coef_.tolist(),
                'intercept': model.intercept_,
                'mse': mse,
                'r2': r2,
                'plot': 'regression_result.png'
            }
        except Exception as e:
            return f"Error in regression: {str(e)}"