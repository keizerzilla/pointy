import sys
from pointy import PointCloud

if len(sys.argv) != 4:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 demo_axialseg.py <[str]caminho_nuvem> <[int]eixo{0 : x, 1 : y, 2 :z}> <[int]numero_particoes>")
    sys.exit(1)

cloud = PointCloud(file_path=sys.argv[1])
axis = int(sys.argv[2])
n_clusters = int(sys.argv[3])

cloud.axial_segmentation(axis, n_clusters)
cloud.draw_clusters()
