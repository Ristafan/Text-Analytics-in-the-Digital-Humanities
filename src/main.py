from nltk import BigramAssocMeasures, TrigramAssocMeasures, QuadgramAssocMeasures

import src.PreProcessing.JsonPreprocessor as JsonPreprocessor
import src.PreProcessing.NaturalLanguageProcessor as NaturalLanguageProcessor
import src.TextAnalytics.KernelDensity as KernelDensity

import os
from nltk.collocations import *


def preprocess_text(path, posts, time):
    """
    Preprocess the text by loading the posts or comments from a JSON file, normalizing the text, and saving it to a TXT file.
    :param path: Path to the JSON file.
    :param posts: True if the file contains posts, False if it contains comments.
    """
    directory = os.path.dirname(path)
    filename = os.path.basename(path).split('.')[0]

    if posts:
        # Load the posts
        processor = JsonPreprocessor.JsonPreprocessor(path, time)
        processor.open_json_file()
        posts = processor.parse_reddit_posts()
        txt = processor.return_plain_text(posts)
        print(f"Number of posts: {len(posts)}")
    else:
        # Load the comments
        processor = JsonPreprocessor.JsonPreprocessor(path, time)
        processor.open_json_file()
        posts = processor.parse_reddit_comments()
        txt = processor.return_plain_text(posts)
        print(f"Number of comments: {len(posts)}")

    # Normalize the text
    nlp = NaturalLanguageProcessor.NaturalLanguageProcessor(txt)
    nlp.save_txt(os.path.join(directory, f"{filename}.txt"))
    print("Text normalized and saved")

def combine_text_files(directory, filename1, filename2):
    """
    Combine two text files into one.
    :param directory: Directory where the text files are located.
    :param filename1: Name of the first text file.
    :param filename2: Name of the second text file.
    """
    with open(os.path.join(directory, f"{filename1}.txt"), 'r', encoding='utf-8') as f1, \
         open(os.path.join(directory, f"{filename2}.txt"), 'r', encoding='utf-8') as f2, \
         open(os.path.join(directory, f"{filename1}_{filename2}_combined.txt.txt"), 'w', encoding='utf-8') as outfile:
        outfile.write(f1.read() + "\n" + f2.read())


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

        # --- Bigram Collocations ---
        print("\n--- Bigram Collocations ---")
        bigram_filter = max(len(words) // 1000, 2)  # Start with a reasonable initial filter
        coll2 = []
        while len(coll2) < 10 and bigram_filter > 1:
            bigram_finder = BigramCollocationFinder.from_words(words)
            bigram_finder.apply_freq_filter(bigram_filter)
            coll2 = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 30)  # Keep a limit
            print(f"Bigram filter: {bigram_filter}, Results: {len(coll2)}")
            bigram_filter -= max(len(words) // 10000, 2)  # Decrease the filter
        coll.append(coll2)
        print(coll2)

        # --- Trigram Collocations ---
        print("\n--- Trigram Collocations ---")
        trigram_filter = max(len(words) // 2000, 2)  # Start with a reasonable initial filter
        coll3 = []
        while len(coll3) < 10 and trigram_filter > 1:
            trigram_finder = TrigramCollocationFinder.from_words(words)
            trigram_finder.apply_freq_filter(trigram_filter)
            coll3 = trigram_finder.nbest(TrigramAssocMeasures.likelihood_ratio, 30)  # Keep a limit
            print(f"Trigram filter: {trigram_filter}, Results: {len(coll3)}")
            trigram_filter -= max(len(words) // 10000, 2)  # Decrease the filter
        coll.append(coll3)
        print(coll3)

        # --- Quadgram Collocations ---
        print("\n--- Quadgram Collocations ---")
        fourgram_filter = max(len(words) // 3000, 2)  # Start with a reasonable initial filter
        coll4 = []
        while len(coll4) < 10 and fourgram_filter > 1:
            fourgram_finder = QuadgramCollocationFinder.from_words(words)
            fourgram_finder.apply_freq_filter(fourgram_filter)
            coll4 = fourgram_finder.nbest(QuadgramAssocMeasures.likelihood_ratio, 30)  # Keep a limit
            print(f"Quadgram filter: {fourgram_filter}, Results: {len(coll4)}")
            fourgram_filter -= max(len(words) // 10000, 2)  # Decrease the filter
        coll.append(coll4)
        print(coll4)

    # Save collocations to a file
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
    directory = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights'
    posts_filename_after = 'r_MensRights_posts(afterElection).jsonl'
    comments_filename_after = 'r_MensRights_comments(afterElection).jsonl'

    posts_filename_before = 'r_MensRights_posts(beforeElection).jsonl'
    comments_filename_before = 'r_MensRights_comments(beforeElection).jsonl'

    combined_posts_filename = f"{posts_filename_after[:-6]}_{posts_filename_before[:-6]}_combined.txt"
    combined_comments_filename = f"{comments_filename_after[:-6]}_{comments_filename_before[:-6]}_combined.txt"

    # Preprocess the text
    preprocess_text(os.path.join(directory, posts_filename_before), True, "beforeTheElection")
    preprocess_text(os.path.join(directory, comments_filename_before), False, "beforeTheElection")
    preprocess_text(os.path.join(directory, posts_filename_after), True, "afterTheElection")
    preprocess_text(os.path.join(directory, comments_filename_after), False, "afterTheElection")

    # Append the posts and comments from the second set of files
    combine_text_files(directory, posts_filename_after[:-6], posts_filename_before[:-6])  # Remove '.jsonl' from filename
    combine_text_files(directory, comments_filename_after[:-6], comments_filename_before[:-6])  # Remove '.jsonl' from filename

    # Generate Kernel Density Estimation for posts and comments
    kernelDensityEstimation(directory, combined_posts_filename)
    kernelDensityEstimation(directory, combined_comments_filename)

    # Generate word collocations for posts and comments
    # wordCollolcations(directory, posts_filename)
    # wordCollolcations(directory, comments_filename)
