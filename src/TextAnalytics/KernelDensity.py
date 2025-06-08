from textplot.helpers import build_graph
import os


class KernelDensity:
    def __init__(self, file_path, term_depth=500, skim_depth=7, d_weights=False):
        self.file_path = file_path
        self.path = os.path.dirname(file_path)
        self.term_depth = term_depth
        self.skim_depth = skim_depth
        self.d_weights = d_weights
        self.graph = None

    def build_graph(self, **kwargs):
        self.graph = build_graph(self.file_path, term_depth=self.term_depth, skim_depth=self.skim_depth, d_weights=self.d_weights, **kwargs)

    def save_graph(self, name):
        self.graph.write_graphml(os.path.join(self.path, name + '.graphml'))


if __name__ == "__main__":
    # Example usage
    path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/test.txt'
    kernel_density = KernelDensity(path)
    kernel_density.build_graph()
    kernel_density.save_graph("test1")
