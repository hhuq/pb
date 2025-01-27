import pickle
import pandas as pd
from collections import defaultdict

# 假设load_data_from_mysql已经定义好，能够读取数据
# from your_module import load_data_from_mysql

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes  # {'node': {'type': 'type_value'}}
        self.edges = edges  # [('node1', 'node2', {'weight': weight}), ...]

class NodeClustering:
    def __init__(self, communities, graph):
        self.communities = communities  # List of communities (each community is a list of nodes)
        self.graph = graph  # Graph object representing the network structure

def get_node_types():
    """获取所有节点的type信息"""
    # 假设 'filter_api_data' 表包含所有节点的独热编码信息和对应的类型
    filter_api_data = load_data_from_mysql("filter_api_data")  # 读取节点类型数据
    
    # 构建节点类型的映射
    node_types = {}
    for _, row in filter_api_data.iterrows():
        node_name = row['Name']
        # 通过独热编码字段为节点分配type
        for col in filter_api_data.columns:
            if col.startswith('Primary Category_') and row[col] == 1:
                node_types[node_name] = col.split('_')[2]  # 提取分类名称
                break
    return node_types

def process_communities():
    """处理所有年份的社区结构和图数据，最终保存为pkl文件"""
    all_snapshots = []
    node_types = get_node_types()  # 获取节点类型

    # 遍历每一年的数据，从2005到2020年
    for year in range(2005, 2021):
        print(f"Processing data for {year}...")
        
        # 从数据库读取每年网络和社区划分数据
        network_df = load_data_from_mysql(f"api_net_{year}")
        community_df = load_data_from_mysql(f"{year}_community_detect")
        
        # 构建图
        edges = [(row['api1'], row['api2'], {'weight': row['weight']}) for _, row in network_df.iterrows()]
        nodes = {}
        
        for node in set(network_df['api1']).union(set(network_df['api2'])):
            # 获取每个节点的type属性
            if node in node_types:
                nodes[node] = {'type': node_types[node]}  # 根据节点名称获取type
            else:
                nodes[node] = {'type': 'Unknown'}  # 如果没有类型，默认标记为'Unknown'
        
        graph = Graph(nodes=nodes, edges=edges)
        
        # 构建社区列表
        communities = defaultdict(list)
        for _, row in community_df.iterrows():
            communities[row['Community']].append(row['API'])
        
        # 将社区数据转化为列表
        community_list = list(communities.values())
        
        # 创建NodeClustering对象
        node_clustering = NodeClustering(communities=community_list, graph=graph)
        all_snapshots.append(node_clustering)
    
    # 将所有社区快照保存为pkl文件
    with open('pb_communities.pkl', 'wb') as f:
        pickle.dump(all_snapshots, f)
    
    print("Data has been saved to pb_communities.pkl.")

# 主函数入口，调用处理函数
if __name__ == "__main__":
    process_communities()
