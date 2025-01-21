import pickle
import mysql.connector
import networkx as nx
from cdlib import algorithms
from pb.mysql_config import load_data_from_mysql

def generate_snapshots(edges_data, nodes_data, year):
    """
    生成快照
    """
    # 创建图对象
    snapshot = nx.Graph()

    # 获取所有在边数据中出现的节点
    involved_nodes = set()
    for _, edge in edges_data.iterrows():
        api1 = edge["api1"]
        api2 = edge["api2"]
        involved_nodes.add(api1)
        involved_nodes.add(api2)

    # 只添加参与边的节点
    for _, node in nodes_data.iterrows():
        if node["Name"] in involved_nodes:  # 只添加在边数据中出现的节点
            snapshot.add_node(node["Name"], type=node["Primary Category"])

    # 添加边
    for _, edge in edges_data.iterrows():
        api1 = edge["api1"]
        api2 = edge["api2"]
        weight = edge["weight"]
        if api1 in snapshot.nodes and api2 in snapshot.nodes:  # 确保边的两个节点都在图中
            snapshot.add_edge(api1, api2, weight=weight)

    # 输出调试信息
    print(f"================={year}===================")
    print(f"{year} 年 生成的快照中有 {len(snapshot.nodes)} 个节点，{len(snapshot.edges)} 条边。")
    print(f"{year} 年 第一个节点的信息：{list(snapshot.nodes(data=True))[0]}")
    print(f"{year} 年 第一个边的信息：{list(snapshot.edges(data=True))[0]}\n")

    return snapshot


def process_data(pkl=None):
    """
    处理数据并生成快照，或者从已有的 pkl 文件加载快照
    """
    snapshots = []  # 用于存储所有快照
    timestamps = []  # 用于存储对应的时间戳

    if pkl is not None:
        print(f"Loading snapshots from {pkl}")
        snapshots_dict = pickle.load(open(pkl, "rb"))
        return snapshots_dict  # 返回已加载的快照字典

    # 获取2005到2020年的边数据
    for year in range(2005, 2021):
        # 获取当前年份的边数据
        edges_data = load_data_from_mysql(f"api_net_{year}")
        # 获取节点数据
        nodes_data = load_data_from_mysql(f"filter_api_data")
        # 创建快照
        snapshot = generate_snapshots(edges_data, nodes_data, year)
        # 添加快照和时间戳到列表中
        snapshots.append(snapshot)
        timestamps.append(f"{year}-12-31")

    # 打印调试信息
    print("=================all===================")
    print(f"生成的快照总数: {len(snapshots)}")
    print(f"第一个快照的节点: {list(snapshots[0].nodes)}")
    print(f"第一个快照的边: {list(snapshots[0].edges)}")
    print(f"第一个快照的所有节点信息: {list(snapshots[0].nodes(data=True))}")
    print(f"第一个快照的所有边信息: {list(snapshots[0].edges(data=True))}")

    # 将快照和时间戳封装成字典并保存为 pkl 文件
    snapshots_dict = {"snapshots": snapshots, "timestamps": timestamps}
    pickle.dump(snapshots_dict, open("data/pb_snapshots.pkl", "wb"))
    print("pb_snapshots.pkl 已保存。")

    return snapshots_dict  # 返回字典格式


if __name__ == "__main__":
    process_data()  # 可以传入 pkl 文件路径，若为空，则生成新的快照数据
