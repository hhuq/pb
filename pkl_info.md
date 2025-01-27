### communities.pkl

`communities.pkl` 是一个列表，列表的每个元素表示一个快照的社区结构。每个元素是一个 `NodeClustering` 对象，该对象包含以下内容：

- `communities`：一个列表，其中包含多个社区，每个社区是一个节点列表，代表了该社区中的所有节点。
- `graph`：一个图对象，表示当前快照的图，包含节点信息（如 `type`）和边信息（如 `weight`）。

社区结构示例：

```python
[
    NodeClustering(communities=[['Ola', '印度打车应用', '打车公司'], ['骑电单车', '共享电单车平台', '闪骑电单车'], ...], 
                    graph=Graph(nodes={'Ola': {'type': 'Service'}, ...}, edges=[('Ola', '印度打车应用', {'weight': 0.5}), ...])),
    NodeClustering(communities=[['知乎', '小蓝星推荐', '消费决策参考'], ...], 
                    graph=Graph(nodes={'知乎': {'type': 'Content'}, ...}, edges=[('知乎', '小蓝星推荐', {'weight': 0.8}), ...])),
    NodeClustering(communities=[['Bounce', '印度摩托车租赁公司', '在线摩托车租赁服务商'], ...], 
                    graph=Graph(nodes={'Bounce': {'type': 'Service'}, ...}, edges=[('Bounce', '印度摩托车租赁公司', {'weight': 0.7}), ...]))
]
```

输出的调试信息：

```
--------------------------------------------------
NodeClustering 42:
  Communities: [...['魔方', '人工智能平台', 'AI平台'], ['Bounce', '印度摩托车租赁公司', '在线摩托车租赁服务商'], ['谷歌地图', '共享单车数据', '站点及数量'], ['LVMH', 'Rapha', '单车装备品牌'], ['云厨房', '卡兰尼克', '张严琪']]
  Graph nodes: 415
  Graph edges: 447
  Node details (showing first 3 nodes):
    Node HappyCycle: {'type': 'Stakeholder'}
    Node Pre-A轮融资: {'type': 'Service'}
    Node 动感单车健身品牌: {'type': 'Service'}
  Edge details (showing first 3 edges):
    Edge (HappyCycle, Pre-A轮融资): {'weight': 0.6048387096774193}
    Edge (HappyCycle, 动感单车健身品牌): {'weight': 2}
    Edge (Pre-A轮融资, 骑呗单车): {'weight': 0.6818181818181819}
```

### social_positions.pkl

social_positions.pkl中文件的组织形式：

list类型

```
[
    {'Google Maps': 0.15, 'del.icio.us': 0.12, 'Microsoft Bing Maps': 0.10, 'Flickr': 0.13, 'FedEx': 0.14},
    {'Google Maps': 0.16, 'del.icio.us': 0.11, 'Microsoft Bing Maps': 0.09, 'Flickr': 0.12, 'FedEx': 0.13},
    {'Google Maps': 0.18, 'del.icio.us': 0.10, 'Microsoft Bing Maps': 0.08, 'Flickr': 0.14, 'FedEx': 0.12},
    ...
]
```

