import sys
import numpy as np
import open3d as o3d
from matplotlib import cm
from pointy import PointCloud

if len(sys.argv) < 2:
    print("ERRO! Número incorreto de parâmetros!")
    print("USO: python3 demo_draw.py <[str]caminho_nuvem_01> <[str]caminho_nuvem_02> ... <[str]caminho_nuvem_N>")
    sys.exit(1)

if len(sys.argv[1:]) > 10:
    print("ERRO! O número máximo de nuvens numa única visualização é 10!")
    sys.exit(1)

color_list = list(cm.get_cmap("tab10").colors)
color_names = ["Azul escuro", "Laranja", "Verde", "Vermelho", "Roxo", "Marrom", "Rosa", "Cinza", "Musgo", "Azul claro"]

pcd_list = []
for i, cloud_path in enumerate(sys.argv[1:]):
    cloud = PointCloud(file_path=cloud_path)
    cloud.pcd.paint_uniform_color(color_list[i])
    pcd_list.append(cloud.pcd)
    print(f"{cloud_path} -> {color_names[i]}")

o3d.visualization.draw_geometries(pcd_list, width=800, height=600, window_name="demo_draw.py")

