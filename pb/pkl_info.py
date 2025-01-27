import pickle
import networkx as nx

# 子函数：处理 communities.pkl 文件
def process_communities_pkl(x):
    print("communities.pkl 中的数据是列表，内容如下:")
    for idx, item in enumerate(x):
        print(f"NodeClustering {idx + 1}:")
        
        # 查看每个 NodeClustering 对象的 communities 属性
        if hasattr(item, 'communities'):
            print(f"  Communities: {item.communities}")
        
        # 如果有 graph 属性，输出图的信息
        if hasattr(item, 'graph'):
            print(f"  Graph nodes: {len(item.graph.nodes)}")
            print(f"  Graph edges: {len(item.graph.edges)}")
            
            # 输出前三个节点的详细信息
            print("  Node details (showing first 3 nodes):")
            for i, (node, data) in enumerate(item.graph.nodes(data=True)):
                if i >= 3:
                    break
                print(f"    Node {node}: {data}")
            
            # 输出前三条边的详细信息
            print("  Edge details (showing first 3 edges):")
            for i, (u, v, data) in enumerate(item.graph.edges(data=True)):
                if i >= 3:
                    break
                print(f"    Edge ({u}, {v}): {data}")
        
        print("-" * 50)


# 子函数：处理字典类型 pkl 文件
def process_dict_pkl(x):
    print("### 字典内容分析 ###")
    
    # 输出字典的键
    print(f"字典的键: {x.keys()}")
    
    # 输出字典的内容
    print(f"字典的内容: {x}")
    
    # 输出时间戳信息
    if 'timestamps' in x:
        print("\n### 时间戳信息 ###")
        print(f"时间戳: {x['timestamps']}")

    # 如果字典中包含 'snapshots' 键
    if 'snapshots' in x:
        print("\n### Snapshots 详细信息 (前五个节点/边) ###")
        snapshot = x['snapshots'][0]  # 选择第一个图
        print(f"第一个图的节点: {list(snapshot.nodes)[:5]}")  # 只输出前 5 个节点
        print(f"第一个图的边: {list(snapshot.edges)[:5]}")  # 只输出前 5 条边
        
        # 输出前三个节点信息
        print("\n#### 节点信息 (前 3 个) ####")
        for idx, (node, attr) in enumerate(snapshot.nodes(data=True)):
            if idx >= 3:  # 只显示前 3 个节点
                break
            print(f"  Node {node}: {attr}")

        # 输出前三条边信息
        print("\n#### 边信息 (前 3 条) ####")
        for idx, (u, v, attr) in enumerate(snapshot.edges(data=True)):
            if idx >= 3:  # 只显示前 3 条边
                break
            print(f"  Edge ({u}, {v}): {attr}")
    
    print("-" * 50)


def process_social_position_pkl(social_positions):
    """
    加载并输出 social_positions.pkl 文件中的数据
    """
    print(f"数据类型: {type(social_positions)}")
    
    # 输出每个快照的社交位置分数，限制显示前 5 个节点
    for idx, snapshot_scores in enumerate(social_positions):
        print(f"\n快照 {idx + 1} 的社交位置分数：")
        
        # 获取前 5 个节点的社交位置分数
        top_5 = list(snapshot_scores.items())[:5]
        
        # 只输出前 5 个节点
        for node, score in top_5:
            print(f"  Node {node}: {score}")
    
    print("-" * 50)


# 主函数：加载并处理 pkl 文件
def load_and_process_pkl(file_path):
    # 加载 pkl 文件
    with open(file_path, 'rb') as f:
        x = pickle.load(f)

    # 查看数据类型
    print(f"Loaded {file_path}, Data type:", type(x))

    # 根据文件名选择不同的处理方式
    if 'communities.pkl' in file_path:
        process_communities_pkl(x)
    elif 'pb_social_positions.pkl' in file_path:
        process_social_position_pkl(x)
    elif isinstance(x, dict):
        process_dict_pkl(x)
    else:
        print(f"未定义的文件类型: {file_path} 中的数据类型 {type(x)}")

# 处理具体的文件
# load_and_process_pkl('data/snapshots.pkl')  # 处理snapshots.pkl
# load_and_process_pkl('data/communities.pkl')  # 加载并处理 communities.pkl

load_and_process_pkl('data_pb/pb_social_positions.pkl')
