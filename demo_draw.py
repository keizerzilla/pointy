import sys
from pointy import PointCloud

if len(sys.argv) != 2:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 <[str]caminho_nuvem>")
    sys.exit(1)

cloud = PointCloud(sys.argv[1])

print(cloud)

cloud.draw()

