import src.PreProcessing.JsonPreprocessor as JsonPreprocessor
import src.PreProcessing.NaturalLanguageProcessor as NaturalLanguageProcessor
import src.TextAnalytics.KernelDensity as KernelDensity

import os

from src.TextAnalytics.TextKernelDensityGraph import TextKernelDensityGraph


def main_posts(posts_path):
    # Load the posts
    pass


def main_comments(comments_path):
    directory = os.path.dirname(comments_path)

    # Load the comments
    processor = JsonPreprocessor.JsonPreprocessor(comments_path)
    processor.open_json_file()
    comments = processor.parse_reddit_comments()
    txt = processor.return_plain_text(comments)
    print(f"Number of comments: {len(comments)}")

    # Normalize the text
    nlp = NaturalLanguageProcessor.NaturalLanguageProcessor(txt)
    nlp.lower()
    nlp.remove_links()
    nlp.remove_stopwords()

    text_graph = TextKernelDensityGraph(window_size=3, min_word_freq=1, bandwidth=0.5)
    graph = text_graph.create_graph(nlp.text)
    # Save the graph to a file
    graph_path = os.path.join(directory, 'graph.graphml')
    text_graph.export_graphml(graph_path)
    print(f"Graph created with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")




if __name__ == "__main__":
    comments_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_comments.jsonl'
    posts_path = '/data/reddit/MensRights/r_MensRights_posts.jsonl'

    main_comments(comments_path)
