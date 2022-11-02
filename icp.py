import sys
from pointy import PointCloud
from pointy import Registration

if len(sys.argv) != 3:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 demo_icp.py <[str]caminho_fonte> <[str]caminho_alvo>")
    sys.exit(1)

source = PointCloud(file_path=sys.argv[1])
target = PointCloud(file_path=sys.argv[2])

print(source)
print(target)

reg = Registration(source, target)
reg.icp_point2point()
reg.show_result()

print(reg)

