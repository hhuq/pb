import json
from datetime import datetime as dt

import numpy as np

from community_operations import *
from generate_snapshots import generate_snapshots
from model_operations import generate_samples, train_prediction_model
from report import evolution_event_distribution_report

if __name__ == '__main__':
    nodes = [json.loads(node)["data"] for node in open("data_pb/pb_nodes.json", encoding="utf8").readlines()]
    edges = [json.loads(edge)["data"] for edge in open("data_pb/pb_edges.json", encoding="utf8").readlines()]
    end_time = dt.strptime("2016-08-01", "%Y-%m-%d")
    # 划分快照
    # snapshots = generate_snapshots(end_time, 30, edges, nodes, "data_pb/pb_snapshots.pkl")
    # programmableweb划分快照：
    snapshots = generate_snapshots(end_time, 30, edges, nodes, "data_pb/pb_snapshots.pkl")

    # 社区特征
    communities = static_community_detection(snapshots, "data_pb/pb_communities.pkl")
    social_positions = social_position_score(snapshots, "data_pb/pb_social_positions.pkl")
    meta_community_network = meta_community_network_generation(
        communities, social_positions, 0.5, 0.5, "data_pb/pb_meta_community_network.pkl"
    )
    features = feature_extraction(snapshots, communities, social_positions, "data_pb/pb_features.pkl")
    # samples = generate_samples(meta_community_network, features, False, relative=False)

    # 模型训练，默认是随机森林
    samples = generate_samples(meta_community_network, features, False, "data_pb/pb_samples.pkl")

    explainer = train_prediction_model(samples["train_X"], samples["train_Y"])
    # explainer = train_prediction_model(samples["train_X"], samples["train_Y"], pkl="data_pb/pb_explainer.pkl")


    # Historical Information report
    shape_values = explainer.shap_values(np.array(samples["train_X"]))
    class_names = ["continuing", "growing", "shrinking", "splitting", "merging", "dissolving"]
    # summary_report(shape_values, FEATURE_NAMES, class_names, True)
    # feature_names = [f'1-{name}' for name in FEATURE_NAMES] + [f'2-{name}' for name in FEATURE_NAMES] + [f'3-{name}' for name in FEATURE_NAMES]
    # summary_report(shape_values, feature_names, class_names, False)
    # for feature_name in FEATURE_NAMES:
    #     for class_name in class_names:
    #         dependency_report(feature_name, class_name, shape_values, samples["train_X"], FEATURE_NAMES, class_names)
    evolution_event_distribution_report(snapshots["timestamps"], meta_community_network)