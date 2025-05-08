import os
import json
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from collections import defaultdict
import re
from stop_words import get_stop_words  # Assuming you have this installed
from src.PreProcessing.NaturalLanguageProcessor import NaturalLanguageProcessor
from src.PreProcessing.PostsCommentsLinker import PostsCommentsLinker


class OverallTfidfComputer:
    def __init__(self, top_n=20, min_df=5, max_df=0.9, stop_words='english'):
        self.top_n = top_n
        self.min_df = min_df
        self.max_df = max_df
        self.stop_words = stop_words
        self.vectorizer = TfidfVectorizer(min_df=self.min_df, max_df=self.max_df, stop_words=self.stop_words)

    def compute_overall_tfidf(self, docs_dict):
        """
        Computes overall TF-IDF scores for all combined texts.

        Args:
            docs_dict (dict): Dictionary of {post_id: combined_text}.

        Returns:
            list: [(keyword, overall_tfidf_score), ...] for the top_n keywords overall.
        """
        corpus = list(docs_dict.values())
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        feature_names = self.vectorizer.get_feature_names_out()

        # Sum TF-IDF scores for each term across all documents
        overall_tfidf_scores = tfidf_matrix.sum(axis=0).A1
        term_scores = zip(feature_names, overall_tfidf_scores)

        # Sort terms by their overall TF-IDF score in descending order
        sorted_terms = sorted(term_scores, key=lambda x: x[1], reverse=True)

        return sorted_terms[:self.top_n]


if __name__ == '__main__':
    posts_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_posts(beforeElection).jsonl'
    comments_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_comments(beforeElection).jsonl'
    output_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/MensRights(before)_linked_data_normalized.json'
    overall_tfidf_output_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/MensRights(before)_overall_tfidf_keywords_normalized.json'

    linker = PostsCommentsLinker(posts_path, comments_path)
    linker.link_comments_to_posts()
    linker.save_linked_data(output_path)

    # Load the normalized linked data from the output file
    with open(output_path, 'r', encoding="utf8") as f:
        linked_data = json.load(f)

    # Normalize the text in the linked data
    for post_id, text in tqdm(linked_data.items(), desc="Normalizing text", unit="post"):
        nlp = NaturalLanguageProcessor(text)
        linked_data[post_id] = nlp.text

    # Compute overall TF-IDF
    tfidf_computer = OverallTfidfComputer(top_n=20)
    overall_tfidf_keywords = tfidf_computer.compute_overall_tfidf(linked_data)

    # Save the overall TF-IDF keywords to a new JSON file
    with open(overall_tfidf_output_path, 'w', encoding="utf8") as f:
        json.dump(overall_tfidf_keywords, f, ensure_ascii=False, indent=4)

    print(f"\nOverall TF-IDF keywords (normalized text) saved to: {overall_tfidf_output_path}")
    print("\nTop Overall Keywords (Normalized Text):")
    for keyword, score in overall_tfidf_keywords:
        print(f"  {keyword}: {score:.4f}")