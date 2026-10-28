# -*- coding: utf-8 -*-
"""Рабочая тетрадь 5. DFS и BFS: обходы, связность, топосорт."""
from collections import deque
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

OUT = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "DejaVu Sans"


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def draw(name, edges, pos, title, directed=False, colors=None, highlight=None):
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_edges_from(edges)
    fig, ax = plt.subplots(figsize=(9.4, 6.6))
    palette = {0: "#f6d56b", 1: "#9fd0f0", 2: "#f0b4b4"}
    if colors:
        node_color = [palette.get(colors.get(n, 0), "#d9d9d9") for n in G.nodes()]
    else:
        node_color = "#b7e1c1" if directed else "#b9dff5"
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=980, node_color=node_color,
                           edgecolors="#333333", linewidths=1.3)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=13, font_weight="bold")
    hl = set()
    if highlight:
        hl = {(u, v) for u, v in highlight}
        if not directed:
            hl |= {(v, u) for u, v in highlight}
    normal = [e for e in G.edges() if e not in hl and (e[1], e[0]) not in hl]
    extra = [e for e in G.edges() if e in hl or (e[1], e[0]) in hl]
    kw = dict(arrows=directed, arrowstyle="-|>", arrowsize=16,
              min_source_margin=16, min_target_margin=16,
              connectionstyle="arc3,rad=0.0")
    if normal:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=normal, width=1.6,
                               edge_color="#555555", **kw)
    if extra:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=extra, width=2.8,
                               edge_color="#c0392b", **kw)
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_axis_off()
    fig.tight_layout()
    save(fig, name)


def dfs_order(graph, start):
    visited = set()
    order = []

    def walk(v):
        visited.add(v)
        order.append(v)
        for nb in graph[v]:
            if nb not in visited:
                walk(nb)

    walk(start)
    return order


def bfs_order(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for nb in graph[v]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order


def components(graph):
    visited = set()
    result = []
    for start in graph:
        if start in visited:
            continue
        comp = []
        stack = [start]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            comp.append(v)
            for nb in reversed(graph[v]):
                if nb not in visited:
                    stack.append(nb)
        result.append(comp)
    return result


def bipartite(graph, nodes):
    """BFS-раскраска одной компоненты. None, если конфликт."""
    start = nodes[0]
    color = {start: 0}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for nb in graph[v]:
            if nb not in color:
                color[nb] = 1 - color[v]
                queue.append(nb)
            elif color[nb] == color[v]:
                return None
    return color


def topo(graph):
    visited = set()
    result = []

    def walk(v):
        visited.add(v)
        for nb in graph.get(v, []):
            if nb not in visited:
                walk(nb)
        result.append(v)

    for v in graph:
        if v not in visited:
            walk(v)
    return result[::-1]


def shortest(graph, start, goal):
    parent = {start: None}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        if v == goal:
            break
        for nb in graph[v]:
            if nb not in parent:
                parent[nb] = v
                queue.append(nb)
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


# ---------- задание 1 ----------
g1 = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6, 7],
    4: [2, 8],
    5: [2, 8],
    6: [3, 9],
    7: [3, 9],
    8: [4, 5, 10],
    9: [6, 7, 10],
    10: [8, 9],
}
print("DFS", dfs_order(g1, 1))
print("BFS", bfs_order(g1, 1))

e1 = [(1, 2), (1, 3), (2, 4), (2, 5), (4, 8), (5, 8), (8, 10),
      (3, 6), (3, 7), (6, 9), (7, 9), (9, 10)]
pos1 = {
    1: (0.0, 2.4), 2: (-1.6, 1.2), 3: (1.6, 1.2),
    4: (-2.6, 0.0), 5: (-0.7, 0.0), 6: (0.7, 0.0), 7: (2.6, 0.0),
    8: (-1.6, -1.2), 9: (1.6, -1.2), 10: (0.0, -2.4),
}
draw("sam_1_graf.png", e1, pos1, "Задание 1. Неориентированный граф, старт — вершина 1")

# ---------- задание 2 ----------
g2 = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"],
    "E": ["F"],
    "F": ["E", "G"],
    "G": ["F"],
    "H": [],
    "I": ["J", "L"],
    "J": ["I", "K"],
    "K": ["J", "L"],
    "L": ["I", "K"],
}
comps = components(g2)
print("components", comps)
colors = {}
for comp in comps:
    col = bipartite(g2, comp)
    print(comp, "bipartite" if col else "NOT", col)
    if col:
        colors.update(col)

e2 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"),
      ("E", "F"), ("F", "G"),
      ("I", "J"), ("J", "K"), ("K", "L"), ("L", "I")]
pos2 = {
    "A": (-4.2, 0.4), "B": (-3.0, 1.6), "C": (-3.0, -0.8), "D": (-1.6, 0.2),
    "E": (-0.2, 1.8), "F": (-0.2, 0.4), "G": (-0.2, -1.0), "H": (1.2, 0.4),
    "I": (2.6, 1.6), "J": (4.0, 1.6), "L": (2.6, -0.6), "K": (4.0, -0.6),
}
draw("sam_2_graf.png", e2 + [("H", "H")], pos2,
     "Задание 2. Четыре компоненты связности")
# isolated H: self-loop hack avoided — draw node by adding a dummy? Graph with only edges misses H.
# redraw properly
G = nx.Graph()
G.add_nodes_from(list("ABCDEFGHIJKL"))
G.add_edges_from(e2)
fig, ax = plt.subplots(figsize=(10.2, 5.6))
nx.draw_networkx_nodes(G, pos2, ax=ax, node_size=900, node_color="#fff4c2",
                       edgecolors="#333", linewidths=1.3)
nx.draw_networkx_labels(G, pos2, ax=ax, font_size=12, font_weight="bold")
nx.draw_networkx_edges(G, pos2, ax=ax, width=1.8, edge_color="#e07a1f")
ax.set_title("Задание 2. Компоненты: {A,B,C,D}, {E,F,G}, {H}, {I,J,K,L}", fontsize=12)
ax.set_axis_off()
fig.tight_layout()
save(fig, "sam_2_graf.png")

fig, ax = plt.subplots(figsize=(10.2, 5.6))
palette = {0: "#9fd0f0", 1: "#f6d56b"}
node_color = []
for n in G.nodes():
    if n in "ABC":
        node_color.append("#f0b4b4")  # треугольник, раскраски нет
    elif n == "D":
        node_color.append("#f0b4b4")
    else:
        node_color.append(palette[colors[n]])
nx.draw_networkx_nodes(G, pos2, ax=ax, node_size=900, node_color=node_color,
                       edgecolors="#333", linewidths=1.3)
nx.draw_networkx_labels(G, pos2, ax=ax, font_size=12, font_weight="bold")
nx.draw_networkx_edges(G, pos2, ax=ax, width=1.8, edge_color="#555")
ax.set_title("Задание 2. Красные — не двудольны; синий/жёлтый — две доли", fontsize=12)
ax.set_axis_off()
fig.tight_layout()
save(fig, "sam_2_color.png")

# ---------- задание 3 ----------
g3 = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["E", "F"],
    "D": ["G"],
    "E": ["G", "H"],
    "F": ["G"],
    "G": [],
    "H": [],
}
print("topo", topo(g3))
path = shortest(g3, "A", "H")
print("path", path, "len", len(path) - 1)

e3 = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "E"),
      ("C", "F"), ("D", "G"), ("E", "G"), ("E", "H"), ("F", "G")]
pos3 = {
    "A": (0.0, 2.6), "B": (-1.6, 1.3), "C": (1.6, 1.3),
    "D": (-2.8, 0.0), "E": (0.0, 0.2), "F": (2.8, 0.0),
    "G": (-1.2, -1.4), "H": (1.4, -1.6),
}
draw("sam_3_graf.png", e3, pos3, "Задание 3. Ориентированный ациклический граф", directed=True)
hl = list(zip(path, path[1:]))
draw("sam_3_path.png", e3, pos3,
     "Задание 3. Кратчайший путь A → B → E → H (3 ребра)",
     directed=True, highlight=hl)

print("done")
