import sys
import itertools
from pointy import PointCloud
from pointy import Registration

if len(sys.argv) != 4:
    print("ERRO! Número incorreto de parâmetros!"),
    print("USO: python3 <[str]caminho_fonte> <[str]caminho_alvo> <[int]numero_particoes>")
    sys.exit(1)

source = PointCloud(file_path=sys.argv[1])
target = PointCloud(file_path=sys.argv[2])
n_clusters = int(sys.argv[3])

source.kmeans(n_clusters)
target.kmeans(n_clusters)

for i, j in itertools.product(range(n_clusters), range(n_clusters)):
    src = source.subcloud(i)
    tgt = target.subcloud(j)
    
    reg = Registration(src, tgt)
    reg.icp_point2point()
    
    print(i, "vs", j)
    print(reg)
    print()
    
    reg.show_result()

