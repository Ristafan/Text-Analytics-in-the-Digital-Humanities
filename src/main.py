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

    with open(os.path.join(directory, f"{filename}.txt"), 'r', encoding='utf-8') as f:
        text_content = f.read()

        # Split the text into words
        # This assumes words are separated by whitespace.
        # For more advanced tokenization (handling punctuation, etc.),
        # consider using nltk.word_tokenize
        words = text_content.split()
        # from nltk.tokenize import word_tokenize
        # words = word_tokenize(text_content.lower()) # Example with NLTK tokenizer and lowercasing

        if not words:
            print(f"Warning: The file {filename}.txt seems to be empty or contains no words after splitting.")
            return

        print(f"Number of words found: {len(words)}")
        if len(words) < 4: # Or some other threshold depending on n-gram size
             print(f"Warning: Not enough words for some n-gram calculations. Found: {len(words)}")

        # Create Bigram collocations
        print("\n--- Bigram Collocations ---")
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigram_finder.apply_freq_filter(3) # Ensure this filter is appropriate for your dataset size
        # You might want to check if bigram_finder.word_fd is empty after filtering
        # or if len(bigram_finder.score_ngrams(BigramAssocMeasures.likelihood_ratio)) is 0
        coll2 = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 30)
        coll.append(coll2)
        print(coll2)

        # Create Trigram collocations
        print("\n--- Trigram Collocations ---")
        trigram_finder = TrigramCollocationFinder.from_words(words)
        trigram_finder.apply_freq_filter(3)
        coll3 = trigram_finder.nbest(TrigramAssocMeasures.likelihood_ratio, 30)
        coll.append(coll3)
        print(coll3)

        # Create Quadgram collocations
        # NLTK uses TrigramAssocMeasures for Quadgrams as well.
        print("\n--- Quadgram Collocations ---")
        fourgram_finder = QuadgramCollocationFinder.from_words(words)
        fourgram_finder.apply_freq_filter(3)
        coll4 = fourgram_finder.nbest(QuadgramAssocMeasures.likelihood_ratio, 30) # Or BigramAssocMeasures
        coll.append(coll4)
        print(coll4)

    # If you intend to save 'coll' to a file, you'd do it here.
    # For example:
    with open(os.path.join(directory, f"{filename}_collocations.txt"), 'w', encoding='utf-8') as outfile:
        outfile.write("Bigrams:\n")
        for item in coll2:
            outfile.write(f"{item}\n")
        outfile.write("\nTrigrams:\n")
        for item in coll3:
            outfile.write(f"{item}\n")
        outfile.write("\nQuadgrams:\n")
        for item in coll4:
            outfile.write(f"{item}\n")


if __name__ == "__main__":
    directory = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/lgbt'
    posts_filename = 'r_lgbt_posts(afterElection)'
    comments_filename = 'r_lgbt_comments(afterElection)'

    # Preprocess the text
    # preprocess_text(os.path.join(directory, posts_filename), True)
    # preprocess_text(os.path.join(directory, comments_filename), False)

    # Generate Kernel Density Estimation for posts and comments
    # kernelDensityEstimation(directory, posts_filename)
    # kernelDensityEstimation(directory, comments_filename)

    # Generate word collocations for posts and comments
    wordCollolcations(directory, posts_filename)
    wordCollolcations(directory, comments_filename)
