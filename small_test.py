import networkx as nx
from cdlib import algorithms

# 创建一个简单的示例图
G = nx.Graph()
G.add_edge(1, 2, weight=5)
G.add_edge(2, 3, weight=3)
G.add_edge(3, 4, weight=2)

# 调用 Louvain 算法
result = algorithms.louvain(G, 'weight')
print(result)
