import src.PreProcessing.JsonPreprocessor as JsonPreprocessor
import src.PreProcessing.NaturalLanguageProcessor as NaturalLanguageProcessor
import src.TextAnalytics.KernelDensity as KernelDensity

import os


def main(path, posts):  # True if posts, False if comments
    # Load the posts
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
    nlp.lower()
    nlp.remove_links()
    nlp.remove_stopwords()
    nlp.save_txt(os.path.join(directory, f"{filename}.txt"))
    print("Text normalized and saved")

    # Create the kernel density graph
    kernel_density = KernelDensity.KernelDensity(os.path.join(directory, f"{filename}.txt"))
    kernel_density.build_graph()
    kernel_density.save_graph(os.path.join(directory, filename))


if __name__ == "__main__":
    posts_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/Feminism/r_Feminism_posts.jsonl'
    comments_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/Feminism/r_Feminism_comments(beforeElection).jsonl'

    # main(posts_path, True)
    main(comments_path, False)
