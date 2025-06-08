import networkx as nx

# Parameters
input_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/Feminism/r_Feminism_posts(afterElection)_r_Feminism_posts(beforeElection)_combined.txt.graphml'
output_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/Feminism/a.graphml'
keywords = {"beforetheelection", "aftertheelection"}
multiplicator = 15.0  # Change to 5.0, 10.0 etc. as needed

# Load the graph
G = nx.read_graphml(input_path)

# Multiply weights for edges connected to the keyword nodes
for u, v, data in G.edges(data=True):
    if 'weight' in data:
        if u in keywords or v in keywords:
            try:
                weight = float(data['weight'])
                data['weight'] = str(weight * multiplicator)
            except ValueError:
                pass  # Skip if weight is not numeric

# Save the modified graph
nx.write_graphml(G, output_path)

print(f"Modified graph saved to {output_path}")
