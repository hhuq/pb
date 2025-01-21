import pickle
import networkx as nx

# 加载 pkl 文件
with open('data/pb_snapshots.pkl', 'rb') as f:
    x = pickle.load(f)

# 查看数据类型
print(type(x))

# 如果是字典，查看其中的键值对
if isinstance(x, dict):
    print("字典的键:", x.keys())
    # print("字典的内容:", x)

    # 查看第一个图的结构
    if 'snapshots' in x:
        snapshot = x['snapshots'][0]  # 选择第一个图
        print("第一个图的节点:", snapshot.nodes)
        print("第一个图的边:", snapshot.edges)
        print("Nodes in snapshot:")
        for node, attr in snapshot.nodes(data=True):
            print(f"Node {node}: {attr}")
        print("Edges in snapshot:")
        for u, v, attr in snapshot.edges(data=True):
            print(f"Edge ({u}, {v}): {attr}")
