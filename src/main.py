from nltk import BigramAssocMeasures, TrigramAssocMeasures, QuadgramAssocMeasures

import src.PreProcessing.JsonPreprocessor as JsonPreprocessor
import src.PreProcessing.NaturalLanguageProcessor as NaturalLanguageProcessor
import src.TextAnalytics.KernelDensity as KernelDensity

import os
import nltk
from nltk.collocations import *


def preprocess_text(path, posts):
    """
    Preprocess the text by loading the posts or comments from a JSON file, normalizing the text, and saving it to a TXT file.
    :param path: Path to the JSON file.
    :param posts: True if the file contains posts, False if it contains comments.
    """
    directory = os.path.dirname(path)
    filename = os.path.basename(path).split('.')[0]

    if posts:
        # Load the posts
        processor = JsonPreprocessor.JsonPreprocessor(path)
        processor.open_json_file()
        posts = processor.parse_reddit_posts()
        txt = processor.return_plain_text(posts)
        print(f"Number of posts: {len(posts)}")
    else:
        # Load the comments
        processor = JsonPreprocessor.JsonPreprocessor(path)
        processor.open_json_file()
        posts = processor.parse_reddit_comments()
        txt = processor.return_plain_text(posts)
        print(f"Number of comments: {len(posts)}")

    # Normalize the text
    nlp = NaturalLanguageProcessor.NaturalLanguageProcessor(txt)
    nlp.save_txt(os.path.join(directory, f"{filename}.txt"))
    print("Text normalized and saved")


def kernelDensityEstimation(directory, filename):
    """
    Generate Kernel Density Estimation for the given text file and save it to a new file.
    :param directory:
    :param filename:
    :return:
    """
    # Create the kernel density graph
    kernel_density = KernelDensity.KernelDensity(os.path.join(directory, f"{filename}.txt"))
    kernel_density.build_graph()
    kernel_density.save_graph(os.path.join(directory, filename))


def wordCollolcations(directory, filename):
    """
    Generate word collocations for the given text file and save them to a new file.
    :param directory:
    :param filename:
    """
    coll = []

    with open(os.path.join(directory, f"{filename}.txt")) as f:
        text = f.read()
        # Create Bigram collocations
        bigram_collocation = BigramCollocationFinder.from_words(text)
        bigram_collocation.apply_freq_filter(3)
        coll2 = bigram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 30)
        coll.append(coll2)
        print(coll2)

        # Create Trigram collocations
        trigram_collocation = TrigramCollocationFinder.from_words(text)
        trigram_collocation.apply_freq_filter(3)
        coll3 = trigram_collocation.nbest(TrigramAssocMeasures.likelihood_ratio, 30)
        coll.append(coll3)
        print(coll3)

        # Create Quadgram collocations
        fourgram_collocation = QuadgramCollocationFinder.from_words(text)
        fourgram_collocation.apply_freq_filter(3)
        coll4 = fourgram_collocation.nbest(QuadgramAssocMeasures.likelihood_ratio, 30)
        coll.append(coll4)
        print(coll4)

    with open(os.path.join(directory, f"coll_{filename}.txt"), 'w') as f:
        for i in coll:
            f.write(str(i))
            f.write('\n')


if __name__ == "__main__":
    directory = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/lgbt'
    posts_filename = 'r_lgbt_posts(afterElection).jsonl'
    comments_filename = 'r_lgbt_comments(afterElection).jsonl'

    # Preprocess the text
    preprocess_text(os.path.join(directory, posts_filename), True)
    preprocess_text(os.path.join(directory, comments_filename), False)

    # Generate Kernel Density Estimation for posts and comments
    kernelDensityEstimation(directory, posts_filename)
    kernelDensityEstimation(directory, comments_filename)

    # Generate word collocations for posts and comments
