from ..base_tool import BaseTool
from aj_mas.utils import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizerTool(BaseTool):
    def __init__(self):
        super().__init__("Data Visualizer", "Create visualizations from data")

    def execute(self, data: pd.DataFrame, plot_type: str, x_column: str, y_column: str, output_path: str):
        logger.log(f"Executing Data Visualizer Tool")
        try:
            plt.figure(figsize=(10, 6))
            if plot_type == 'scatter':
                sns.scatterplot(data=data, x=x_column, y=y_column)
            elif plot_type == 'line':
                sns.lineplot(data=data, x=x_column, y=y_column)
            elif plot_type == 'bar':
                sns.barplot(data=data, x=x_column, y=y_column)
            else:
                return f"Unsupported plot type: {plot_type}"
            
            plt.title(f"{plot_type.capitalize()} Plot of {y_column} vs {x_column}")
            plt.savefig(output_path)
            plt.close()
            return f"Visualization saved to {output_path}"
        except Exception as e:
            return f"Error creating visualization: {str(e)}"