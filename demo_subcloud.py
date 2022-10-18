import sys
from pointy import PointCloud

if len(sys.argv) != 4:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 <[str]caminho_nuvem> <[int]numero_particoes> <[int]particao_alvo>")
    sys.exit(1)

cloud = PointCloud(file_path=sys.argv[1])
n_clusters = int(sys.argv[2])
label = int(sys.argv[3])

cloud.kmeans(n_clusters)
sub = cloud.subcloud(label)

print(sub)

sub.draw()

