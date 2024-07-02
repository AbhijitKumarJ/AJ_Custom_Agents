from ..base_tool import BaseTool
from aj_mas.utils import logger
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt

class FeatureImportanceTool(BaseTool):
    def __init__(self):
        super().__init__("Feature Importance", "Calculate feature importance using Random Forest")

    def execute(self, X: np.array, y: np.array, feature_names: list):
        logger.log(f"Executing Feature Importance Tool")
        try:
            model = RandomForestRegressor()
            model.fit(X, y)
            
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 6))
            plt.title("Feature Importances")
            plt.bar(range(X.shape[1]), importances[indices])
            plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
            plt.tight_layout()
            plt.savefig('feature_importance.png')
            plt.close()

            return {
                'feature_importance': dict(zip(feature_names, importances.tolist())),
                'plot': 'feature_importance.png'
            }
        except Exception as e:
            return f"Error in calculating feature importance: {str(e)}"