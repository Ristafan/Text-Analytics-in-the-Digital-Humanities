import src.PreProcessing.JsonPreprocessor as JsonPreprocessor
import src.PreProcessing.NaturalLanguageProcessor as NaturalLanguageProcessor
import src.TextAnalytics.KernelDensity as KernelDensity

import os



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

    # Create the kernel density graph



if __name__ == "__main__":
    comments_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_comments.jsonl'
    posts_path = '/data/reddit/MensRights/r_MensRights_posts.jsonl'

    # main_comments(comments_path)

