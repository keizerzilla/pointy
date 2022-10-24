import sys
from pointy import PointCloud

if len(sys.argv) != 2:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 demo_draw.py <[str]caminho_nuvem>")
    sys.exit(1)

cloud = PointCloud(file_path=sys.argv[1])

print(cloud)

cloud.draw()

