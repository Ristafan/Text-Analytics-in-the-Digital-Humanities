import numpy as np
import networkx as nx
from sklearn.neighbors import KernelDensity
import re
import string
from collections import Counter
import nltk
from nltk.corpus import stopwords
import os


class TextKernelDensityGraph:
    """
    A class that converts text into a graph using Kernel Density Estimation.
    The graph represents words as nodes and their relationships as edges.
    """

    def __init__(self, window_size=5, min_word_freq=2, bandwidth=0.5):
        """
        Initialize the TextKernelDensityGraph.

        Parameters:
        -----------
        window_size : int
            The size of the sliding window for word co-occurrence
        min_word_freq : int
            Minimum frequency for a word to be included in the graph
        bandwidth : float
            Bandwidth parameter for the KDE
        """
        self.window_size = window_size
        self.min_word_freq = min_word_freq
        self.bandwidth = bandwidth
        self.graph = nx.Graph()

        # Download NLTK resources if not already downloaded
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """
        Preprocess text by lowercasing, removing punctuation and stopwords.

        Parameters:
        -----------
        text : str
            The input text to preprocess

        Returns:
        --------
        list
            List of preprocessed words
        """
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)

        # Split into words and remove stopwords
        words = [word for word in text.split() if word not in self.stop_words and len(word) > 1]

        return words

    def create_graph(self, text):
        """
        Create a graph from the input text.

        Parameters:
        -----------
        text : str
            The input text to process

        Returns:
        --------
        nx.Graph
            The created graph
        """
        # Preprocess text
        words = self.preprocess_text(text)

        # Count word frequencies
        word_freq = Counter(words)

        # Filter words by frequency
        filtered_words = [word for word in words if word_freq[word] >= self.min_word_freq]

        # Create a vocabulary of unique words
        vocab = list(set(filtered_words))
        vocab_dict = {word: i for i, word in enumerate(vocab)}

        # Initialize co-occurrence matrix
        cooccurrence = np.zeros((len(vocab), len(vocab)))

        # Build co-occurrence matrix using sliding window
        for i in range(len(filtered_words)):
            target_word = filtered_words[i]
            if target_word in vocab_dict:
                target_idx = vocab_dict[target_word]

                # Define window boundaries
                window_start = max(0, i - self.window_size)
                window_end = min(len(filtered_words), i + self.window_size + 1)

                # Update co-occurrence counts for words in the window
                for j in range(window_start, window_end):
                    if j != i:  # Skip the target word itself
                        context_word = filtered_words[j]
                        if context_word in vocab_dict:
                            context_idx = vocab_dict[context_word]
                            cooccurrence[target_idx, context_idx] += 1

        # Create a new empty graph
        self.graph = nx.Graph()

        # Add nodes (words) to the graph
        for word in vocab:
            # Add node attributes like frequency
            self.graph.add_node(word, frequency=word_freq[word])

        # Apply KDE to determine edge weights
        for i in range(len(vocab)):
            for j in range(i + 1, len(vocab)):
                if cooccurrence[i, j] > 0:
                    word1 = vocab[i]
                    word2 = vocab[j]

                    # Create feature vector for KDE (can be extended with more features)
                    features = np.array([[cooccurrence[i, j]]])

                    # Apply KDE
                    kde = KernelDensity(bandwidth=self.bandwidth, kernel='gaussian')
                    kde.fit(features)

                    # Calculate weight using KDE density estimate
                    weight = np.exp(kde.score_samples(features)[0])

                    # Add edge if weight is significant
                    if weight > 0.01:  # Threshold can be adjusted
                        self.graph.add_edge(word1, word2, weight=weight)

        return self.graph

    def export_gexf(self, output_path):
        """
        Export the graph to GEXF format for Gephi.

        Parameters:
        -----------
        output_path : str
            Path to save the GEXF file
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            raise ValueError("Graph is empty. Run create_graph method first.")

        nx.write_gexf(self.graph, output_path)
        print(f"Graph exported to {output_path}")

    def export_graphml(self, output_path):
        """
        Export the graph to GraphML format.

        Parameters:
        -----------
        output_path : str
            Path to save the GraphML file
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            raise ValueError("Graph is empty. Run create_graph method first.")

        nx.write_graphml(self.graph, output_path)
        print(f"Graph exported to {output_path}")

    def export_json(self, output_path):
        """
        Export the graph to JSON format compatible with Graphology.

        Parameters:
        -----------
        output_path : str
            Path to save the JSON file
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            raise ValueError("Graph is empty. Run create_graph method first.")

        # Convert NetworkX graph to a dictionary in Graphology compatible format
        graph_dict = {
            "attributes": {},
            "options": {
                "type": "undirected",
                "multi": False
            },
            "nodes": [],
            "edges": []
        }

        # Add nodes
        for node, attrs in self.graph.nodes(data=True):
            node_dict = {
                "key": str(node),
                "attributes": attrs
            }
            graph_dict["nodes"].append(node_dict)

        # Add edges
        edge_id = 0
        for u, v, attrs in self.graph.edges(data=True):
            edge_dict = {
                "key": str(edge_id),
                "source": str(u),
                "target": str(v),
                "attributes": attrs
            }
            graph_dict["edges"].append(edge_dict)
            edge_id += 1

        # Write to JSON file
        import json
        with open(output_path, 'w') as f:
            json.dump(graph_dict, f, indent=2)

        print(f"Graph exported to {output_path}")


# Example usage
if __name__ == "__main__":
    # Sample text
    sample_text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence 
    concerned with the interactions between computers and human language, in particular how to program computers 
    to process and analyze large amounts of natural language data. The goal is a computer capable of "understanding" 
    the contents of documents, including the contextual nuances of the language within them. The technology can then 
    accurately extract information and insights contained in the documents as well as categorize and organize the 
    documents themselves.
    """

    # Create the graph
    text_graph = TextKernelDensityGraph(window_size=3, min_word_freq=1, bandwidth=0.5)
    graph = text_graph.create_graph(sample_text)

    # Output graph statistics
    print(f"Graph created with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")

    # Export to different formats
    text_graph.export_gexf("nlp_graph.gexf")
    text_graph.export_graphml("nlp_graph.graphml")
    text_graph.export_json("nlp_graph.json")