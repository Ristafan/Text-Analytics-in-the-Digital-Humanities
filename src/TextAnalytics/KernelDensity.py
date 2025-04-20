from textplot.helpers import build_graph
import networkx as nx

class KernelDensity:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = None
        self.graph = None

    def save_graph(self):
        save_file_path = self.file_path.replace('.txt', '.gml')
        nx.write_gml(self.graph, save_file_path)
        print(f"Graph saved to: {save_file_path}")

    def generate_graph(self, term_depth=500, skim_depth=10, d_weights=False):
        self.graph = build_graph(self.file_path, term_depth=term_depth, skim_depth=skim_depth, d_weights=d_weights)
        print("Graph generated successfully.")
        print(f"Graph type: {type(self.graph)}") # Let's check the graph type

    def get_degree_centrality(self):
        if self.graph is None:
            raise ValueError("Graph has not been generated. Call generate_graph() first.")
        return nx.degree_centrality(self.graph)

    def save_graphml(self, filename):
        try:
            nx.write_graphml(self.graph, filename)
            print(f"Graph saved to GraphML format: {filename}")
        except Exception as e:
            print(f"Error saving to GraphML: {e}")
            print("Make sure you have the 'lxml' library installed (`pip install lxml`).")


if __name__ == "__main__":
    # Example usage
    file_path = "C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/bible.txt"
    kd = KernelDensity(file_path)

    kd.generate_graph()

    kd.save_graph()

    kd.save_graphml(file_path.replace('.txt', '.graphml'))

    degree_centrality = kd.get_degree_centrality()
    print("Degree Centrality:", degree_centrality)