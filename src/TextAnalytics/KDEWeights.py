import networkx as nx
from collections import deque

def apply_recursive_weighting(G, keywords, base_multiplier=7.0, layers=3, step=2.0):
    visited = set()
    weight_map = {}

    # BFS from each keyword
    for keyword in keywords:
        queue = deque([(keyword, 0)])
        while queue:
            node, depth = queue.popleft()
            if node in visited or depth > layers:
                continue
            visited.add(node)

            # Compute current multiplier
            multiplier = max(1.0, base_multiplier - (depth * step))

            # Store node weight influence
            weight_map[node] = max(weight_map.get(node, 1.0), multiplier)

            # Enqueue neighbors
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

    # Apply the new weights
    for u, v, data in G.edges(data=True):
        if 'weight' in data:
            try:
                weight = float(data['weight'])
                node_multiplier = max(weight_map.get(u, 1.0), weight_map.get(v, 1.0))
                data['weight'] = str(weight * node_multiplier)
            except ValueError:
                continue  # Skip if weight is non-numeric

    return G


# === MAIN ===

# Parameters
input_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/Feminism/r_Feminism_posts(afterElection)_r_Feminism_posts(beforeElection)_combined.txt.graphml'
output_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/Feminism/a.graphml'
keywords = {"beforeelection", "afterelection"}
base_multiplier = 10.0
layers = 5
step = 2.0

# Load, process, save
G = nx.read_graphml(input_path)
G = apply_recursive_weighting(G, keywords, base_multiplier, layers, step)
nx.write_graphml(G, output_path)

print(f"Modified graph saved to {output_path}")
