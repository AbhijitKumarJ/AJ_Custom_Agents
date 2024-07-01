from ..base_tool import BaseTool
from utils.logger import logger
import pandas as pd
import numpy as np

class StatisticalAnalysisTool(BaseTool):
    def __init__(self):
        super().__init__("Statistical Analysis", "Perform statistical analysis on data")

    def execute(self, data: pd.DataFrame, analysis_type: str, column: str = None):
        logger.log(f"Executing Statistical Analysis Tool")
        try:
            if analysis_type == 'summary':
                return data.describe().to_dict()
            elif analysis_type == 'correlation':
                return data.corr().to_dict()
            elif analysis_type == 'column_stats' and column:
                return {
                    'mean': data[column].mean(),
                    'median': data[column].median(),
                    'std': data[column].std(),
                    'min': data[column].min(),
                    'max': data[column].max()
                }
            else:
                return f"Unsupported analysis type or missing column for column_stats"
        except Exception as e:
            return f"Error performing statistical analysis: {str(e)}"