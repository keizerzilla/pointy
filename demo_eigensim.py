import sys
import numpy as np
import seaborn as sns
from pointy import PointCloud
from matplotlib import pyplot as plt
from scipy.spatial import distance_matrix

if len(sys.argv) != 4:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 <[str]caminho_fonte> <[str]caminho_alvo> <[int]numero_particoes>")
    sys.exit(1)

source = PointCloud(file_path=sys.argv[1])
target = PointCloud(file_path=sys.argv[2])
n_clusters = int(sys.argv[3])

source.kmeans(n_clusters)
target.kmeans(n_clusters)

src_geofeats = [source.subcloud(i).geometric_features() for i in range(n_clusters)]
tgt_geofeats = [target.subcloud(i).geometric_features() for i in range(n_clusters)]

dist = distance_matrix(src_geofeats, tgt_geofeats)

sns.set()

sns.heatmap(dist, annot=True, fmt="g")
plt.title("Distância entre partições")
plt.xlabel("Índice da nuvem alvo (target)")
plt.ylabel("Índice da nuvem fonte (source)")
plt.tight_layout()
plt.show()

