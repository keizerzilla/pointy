import os
import sys
import copy
import numpy as np
import pandas as pd
from pathlib import Path
from pointy import PointCloud
from pointy import Registration

# checando número correto de argumentos de linha de comando
if len(sys.argv) != 7:
    print("ERRO! Número incorreto de parâmetros!"),
    print("USO: python3 demo_cross_icp.py <[str]caminho_src> <[str]caminho_tgt> <[int]eixo_src> <[int]eixo_tgt> <[int]num_part_src> <[int]num_part_tgt>")
    sys.exit(1)

# carregando nuvens source e target em memória
source = PointCloud(file_path=sys.argv[1])
target = PointCloud(file_path=sys.argv[2])

# resgatando eixos de corte
axis_src = int(sys.argv[3])
axis_tgt = int(sys.argv[4])

# resgatando número de partições de cada nuvem
n_clusters_src = int(sys.argv[5])
n_clusters_tgt = int(sys.argv[6])

# particionando nuvens source e target
source.axial_segmentation(axis_src, n_clusters_src)
target.axial_segmentation(axis_tgt, n_clusters_tgt)

# gerando informações sobre o experimento: arquivos usado, pasta de resultados e nome do experimento
src_cloud_file = Path(sys.argv[1]).stem
tgt_cloud_file = Path(sys.argv[2]).stem
test_name = f"{src_cloud_file}_{n_clusters_src:02d}-vs-{tgt_cloud_file}_{n_clusters_tgt:02d}"
test_folder = f"resultados/axial_{test_name}"
os.makedirs(test_folder, exist_ok=True)

print(test_name)

# laço principal: executa o ICP para cada par de subnuvens source e target
# a cada iteração, os dados de resultado são registrados e posteriormente salvos em arquivo
dump = []
for i in range(n_clusters_src):
    src = source.subcloud(i)
    src_subcloud_path = os.path.normcase(os.path.join(test_folder, f"{src_cloud_file}_{i:02d}-{n_clusters_src-1:02d}.ply"))
    src.save(src_subcloud_path)
    
    for j in range(n_clusters_tgt):
        tgt = target.subcloud(j)
        
        reg = Registration(src, tgt)
        reg.icp_point2point()
        
        aligned_part_path = os.path.normcase(os.path.join(test_folder, f"part_{src_cloud_file}_{i:02d}-{n_clusters_src-1:02d}_vs_{tgt_cloud_file}-{j:02d}-{n_clusters_tgt-1:02d}.ply"))
        reg.aligned.save(aligned_part_path)
        
        # gera nuvem alinha a partir de cópia da nuvem source original (completa)
        # calcula RMSE global, ou seja, avalia o alinhamento entre as nuvens originais com a matriz de transformação do par atual
        reg_global = Registration(source, target)
        reg_global.coarse_registration(reg.transformation)
        rmse_aligned = reg_global.rmse
        aligned = reg_global.aligned
        
        # salvando subnuvens e nuvem alinhada
        tgt_subcloud_path = os.path.normcase(os.path.join(test_folder, f"{tgt_cloud_file}_{j:02d}-{n_clusters_tgt-1:02d}.ply"))
        tgt.save(tgt_subcloud_path)
        
        aligned_path = os.path.normcase(os.path.join(test_folder, f"aligned_{src_cloud_file}_{i:02d}-{n_clusters_src-1:02d}_vs_{tgt_cloud_file}-{j:02d}-{n_clusters_tgt-1:02d}.ply"))
        aligned.save(aligned_path)
        
        # gerando resultados do experimento atual
        matrix = list(np.ravel(reg.transformation))
        result = [os.path.normcase(sys.argv[1]), os.path.normcase(sys.argv[2]), n_clusters_src, n_clusters_tgt, i, j, reg.has_converged, reg.rmse, rmse_aligned, src_subcloud_path, tgt_subcloud_path, aligned_part_path, aligned_path] + matrix
        dump.append(result)
        
        # debug
        print(f"{i:02d} vs {j:02d} => RMSE_PART = {reg.rmse:.6f} | RMSE_GLOBAL = {rmse_aligned:.6f} | Converged? {reg.has_converged}")

# formatando tabela de resultados: nomes das colunas
t_matrix_cols = [f"t{i}" for i in range(16)]
column_names = ["src_cloud", "tgt_cloud", "num_clusters_src", "num_clusters_tgt", "src_cluster", "tgt_cluster", "has_converged", "rmse_part", "rmse_global", "src_subcloud_path", "tgt_subcloud_path", "aligned_part_path", "aligned_path"]
column_names = column_names + t_matrix_cols

# formatando tabela de resultados num objeto pandas.DataFrame
df = pd.DataFrame(data=dump, columns=column_names)
df.to_csv(os.path.join(test_folder, "results.csv"), index=None)

print(df)
print("Pronto!")
