from ..base_tool import BaseTool
from aj_mas.utils import logger
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

class ClusteringTool(BaseTool):
    def __init__(self):
        super().__init__("Clustering", "Perform KMeans clustering on data")

    def execute(self, data: np.array, n_clusters: int):
        logger.log(f"Executing Clustering Tool")
        try:
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(data)
            
            plt.figure(figsize=(10, 6))
            plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_)
            plt.title('KMeans Clustering')
            plt.savefig('clustering_result.png')
            plt.close()

            return {
                'cluster_centers': kmeans.cluster_centers_.tolist(),
                'labels': kmeans.labels_.tolist(),
                'plot': 'clustering_result.png'
            }
        except Exception as e:
            return f"Error in clustering: {str(e)}"