import os
import sys
import copy
import numpy as np
import pandas as pd
from pathlib import Path
from pointy import PointCloud
from pointy import Registration

# checando número correto de argumentos de linha de comando
if len(sys.argv) != 5:
    print("ERRO! Número incorreto de parâmetros!"),
    print("USO: python3 demo_cross_icp.py <[str]caminho_src> <[str]caminho_tgt> <[int]num_part_src> <[int]num_part_tgt>")
    sys.exit(1)

# carregando nuvens source e target em memória
source = PointCloud(file_path=sys.argv[1])
target = PointCloud(file_path=sys.argv[2])

# resgatando número de partições de cada nuvem
n_clusters_src = int(sys.argv[3])
n_clusters_tgt = int(sys.argv[4])

# particionando nuvens source e target
source.kmeans(n_clusters_src)
target.kmeans(n_clusters_tgt)

# gerando informações sobre o experimento: arquivos usado, pasta de resultados e nome do experimento
src_cloud_file = Path(sys.argv[1]).stem
tgt_cloud_file = Path(sys.argv[2]).stem
test_name = f"{src_cloud_file}[{n_clusters_src:02d}]_vs_{tgt_cloud_file}[{n_clusters_tgt:02d}]"
test_folder = f"resultados/{test_name}"
os.makedirs(test_folder, exist_ok=True)

print(test_name)

# laço principal: executa o ICP para cada par de subnuvens source e target
# a cada iteração, os dados de resultado são registrados e posteriormente salvos em arquivo
dump = []
for i in range(n_clusters_src):
    src = source.subcloud(i)
    for j in range(n_clusters_tgt):
        tgt = target.subcloud(j)
        
        reg = Registration(src, tgt)
        reg.icp_point2point()
        
        # gera nuvem alinha a partir de cópia da nuvem source original (completa)
        aligned = copy.deepcopy(source)
        aligned.transform(reg.transformation)
        
        # salvando subnuvens e nuvem alinhada
        src.save(os.path.join(test_folder, f"{src_cloud_file}[{i+1:02d}|{n_clusters_src:02d}].ply"))
        tgt.save(os.path.join(test_folder, f"{tgt_cloud_file}[{j+1:02d}|{n_clusters_tgt:02d}].ply"))
        aligned.save(os.path.join(test_folder, f"aligned_{src_cloud_file}[{i+1:02d}|{n_clusters_src:02d}]_vs_{tgt_cloud_file}[{j+1:02d}|{n_clusters_tgt:02d}].ply"))
        
        # gerando lista com os valores gerados pelo experimento
        src_cloud = [sys.argv[1]]
        tgt_cloud = [sys.argv[2]]
        num_clusters_src = [n_clusters_src]
        num_clusters_tgt = [n_clusters_tgt]
        src_cluster = [i]
        tgt_cluster = [j]
        rmse = [reg.rmse]
        matrix = list(np.ravel(reg.transformation))
        result = src_cloud + tgt_cloud + num_clusters_src + num_clusters_tgt + src_cluster + tgt_cluster + rmse + matrix
        dump.append(result)
        
        # debug :-)
        print(i, j, "OK!")

# formatando tabela de resultados: nomes das colunas
t_matrix_cols = [f"t{i}" for i in range(16)]
column_names = ["src_cloud",
                "tgt_cloud",
                "num_clusters_src",
                "num_clusters_tgt",
                "src_cluster",
                "tgt_cluster",
                "rmse"] + t_matrix_cols

# formatando tabela de resultados: DataFrame
df = pd.DataFrame(data=dump, columns=column_names)
df.to_csv(os.path.join(test_folder, "results.csv"), index=None)

print(df)
print("Pronto!")

