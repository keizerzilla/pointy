import copy
import numpy as np
import open3d as o3d
from matplotlib import cm
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering


class PointCloud:

    def __init__(self, file_path=None, xyz=None):
        """
        Construtor da classe PointCloud.
        Recebe como parâmetro o caminho para um arquivo contendo uma nuvem ou uma matriz de pontos Nx3.
        
        Atributos
        ---------
            file_path: arquivo original (caso a nuvem tenha sido carrega de um arquivo).
            pcd: objeto Open3D que representa a nuvem.
            xyz: matriz Nx3 para manipulação direta dos pontos.
            n_clusters: número de partições usadas para dividir a nuvem.
            labels: list com as etiquetas de cada ponto após clusterização.
        """
        
        assert file_path is not None or xyz is not None, "O construtor deve receber um arquivo ou uma matriz!"
        
        if file_path is not None:
            self.pcd = o3d.io.read_point_cloud(file_path)
            self.xyz = np.asarray(self.pcd.points)
        elif xyz is not None:
            self.pcd = o3d.geometry.PointCloud()
            self.pcd.points = o3d.utility.Vector3dVector(xyz)
            self.xyz = np.asarray(self.pcd.points)
        else:
            raise Exception("Você deve prover um arquivo ou uma matrix Nx3!")
        
        self.file_path = file_path
        self.n_clusters = None
        self.labels = None
    
    def __str__(self):
        """
        Método que formata as informações da classe num string.
        Usada para debug, permite chamar a função print() passando um objeto da classe.
        """
        
        num_points = np.asarray(self.pcd.points).shape[0]
        
        return f"Nuvem {self.file_path} -> {num_points} pontos"
    
    def save(self, output_path, is_ascii=True):
        """
        Salva nuvem em arquivo.
        Recebe como parâmetro o caminho onde a nuvem deve ficar salva.
        Por padrão, o formato do arquivo é o texto (is_ascii=True); trocar para False salva em binário.
        """
        
        o3d.io.write_point_cloud(output_path, self.pcd, write_ascii=is_ascii)
    
    def kmeans(self, n_clusters=4):
        """
        Executa a clusterização usando o algoritmo k-Médias.
        Recebe como parâmetro o número de grupos (clusters) que se deseja gerar.
        Após execução, o atributo 'labels' é atualizado com as etiquetas ponto a ponto.
        """
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(self.pcd.points)
        
        self.n_clusters = n_clusters
        self.labels = kmeans.labels_
    
    def subcloud(self, label=0):
        """
        Retorna um subconjunto da nuvem de pontos atual como um novo objeto PointCloud.
        Recebe o índice de particionamento a ser usado na amostragem.
        """
        
        if self.labels is None:
            raise Exception("Erro: a nuvem ainda não foi clusterizada!\nInvoque primeiro o método .kmeans() ou similar.")
        
        sub = self.xyz[self.labels == label]
        
        return PointCloud(xyz=sub)
    
    def draw(self):
        """
        Método auxiliar que mostra a nuvem numa janela gráfica.
        A janela já vem com iteratividade padrão: mouse rotaciona, +- troca tamanho dos pontos, etc.
        """
        
        title = f"Nuvem {self.file_path}"
        o3d.visualization.draw_geometries([self.pcd], width=800, height=600, window_name=title)
    
    def draw_clusters(self):
        """
        Método auxiliar que desenha a nuvem, mas destacando os grupos após clusterização.
        Dispara erro caso a clusterização não tenha sido realizada primeiro.
        """
        
        if self.labels is None:
            raise Exception("Erro: a nuvem ainda não foi clusterizada!\nInvoque primeiro o método .kmeans() ou similar.")
        
        color_list = np.array(cm.get_cmap("tab10").colors)
        self.pcd.colors = o3d.utility.Vector3dVector(color_list[self.labels])
        
        title = f"Nuvem {self.file_path} particionada {self.n_clusters} vezes"
        o3d.visualization.draw_geometries([self.pcd], width=800, height=600, window_name=title)
    
    def rotate(self, rotation):
        """
        Método que rotaciona a nuvem.
        Recebe uma lista com três ângulos (em radianos), um para cada rotação em X, Y e Z, respectivamente.
        """
        
        R = self.pcd.get_rotation_matrix_from_xyz(rotation)
        self.pcd.rotate(R)
    
    def transform(self, transformation):
        """
        Aplica transformação geral definida por uma matriz homogênea 4x4.
        """
        
        self.pcd.transform(transformation)


class Registration:
    
    def __init__(self, source, target):
        """
        Classe que representa o registro entre duas nuvens.
        Recebe como parâmetro uma nuvem fonte e outra alvo.
        As nuvens devem ser objetos da classe PointCloud!
        
        Atributos
        ---------
            source: referência da nuvem fonte.
            target: referência da nuvem alvo.
            aligned: referência da nuvem resultado do registro (nuvem alinhada).
            transformation: a transformação (matriz 4x4) que gerou a nuvem alinhada.
            rmse: o erro do alinhamento que gerou a nuvem alinhada.
        """
        
        self.source = source
        self.target = target
        self.aligned = None
        self.transformation = None
        self.rmse = None
    
    def __str__(self):
        """
        Método que formata as informações da classe num string.
        Usada para debug, permite chamar a função print() passando um objeto da classe.
        """
        
        str_source = f"SOURCE: {self.source.file_path}"
        str_target = f"TARGET: {self.target.file_path}"
        str_trans = f"TRANSFORMACAO:\n{self.transformation}"
        str_rmse = f"RMSE: {self.rmse}"
        
        return str_source + "\n" + str_target + "\n" + str_trans + "\n" + str_rmse
    
    def icp_point2point(self, threshold=0.02):
        """
        Método que executa o ICP ponto-a-ponto.
        Único parâmetro passado hoje é a distância máxima de correspondência (padrão: 0.02)
        O parâmetro de número de iterações máximo é o padrão do Open3D: 30.
        Deixei esse método o mais simples possível, fica como exercício expandir os parâmetros.
        Ao final da execução, os atributos 'transformation', 'rmse' e 'aligned' ficam disponíveis.
        """
        
        icp_reg = o3d.pipelines.registration.registration_icp(self.source.pcd, self.target.pcd, threshold)
        
        self.transformation = icp_reg.transformation
        self.rmse = icp_reg.inlier_rmse
        
        aligned = copy.deepcopy(self.source)
        aligned.transform(self.transformation)
        
        self.aligned = aligned
    
    def show_result(self):
        """
        Método auxiliar que mostra resultado do alinhamento.
        Exibe nuvem alvo com pontos coloridos de azul.
        Exibe nuvem alinhada com pontos coloridos de vermelho.
        """
        
        target_copy = copy.deepcopy(self.target.pcd)
        aligned_copy = copy.deepcopy(self.aligned.pcd)
        
        target_copy.paint_uniform_color([0, 0, 1])
        aligned_copy.paint_uniform_color([1, 0, 0])
        
        title = f"Registro: {self.source.file_path} vs {self.target.file_path} (alvo: azul, alinhada: vermelho)"
        o3d.visualization.draw_geometries([target_copy, aligned_copy], width=800, height=600, window_name=title)

