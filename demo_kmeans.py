import sys
from pointy import PointCloud

if len(sys.argv) != 3:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 <[str]caminho_nuvem> <[int]numero_particoes>")
    sys.exit(1)

cloud = PointCloud(sys.argv[1])
n_clusters = int(sys.argv[2])

print(cloud)

cloud.kmeans(n_clusters)
cloud.draw_clusters()

