import os
import json
from tqdm import tqdm


class JsonPreprocessor:
    def __init__(self, file_path, time):
        self.file_path = file_path
        self.time = time
        self.json_list = None
        self.file_data = {}

    def open_json_file(self):
        assert os.path.exists(self.file_path), f'Path to file is incorrect: {self.file_path}'
        with open(self.file_path, 'r', encoding="utf8") as json_file:
            self.json_list = list(json_file)

    def parse_reddit_comments(self):
        """
        Parses the reddit comments from the json file and stores them in a dictionary.
        The keys are the comment IDs and the values are lists containing the comment body.
        :return:
        A dictionary with comment IDs as keys and lists of comment bodies as values.
        """
        for json_str in tqdm(self.json_list, desc="Parsing comments", unit="comment"):
            obj = json.loads(json_str)
            self.file_data[obj['id']] = obj['body'] + " " + self.time
        return self.file_data

    def parse_reddit_posts(self):
        """
        Parses the reddit posts from the json file and stores them in a dictionary.
        The keys are the post IDs and the values are lists containing the post body.
        :return:
        A dictionary with post IDs as keys and lists of post bodies as values.
        """
        for json_str in tqdm(self.json_list, desc="Parsing posts", unit="post"):
            obj = json.loads(json_str)
            self.file_data[obj['id']] = obj['title'] + " " + obj['selftext'] + " " + self.time

        return self.file_data

    @staticmethod
    def return_plain_text(dictionary):
        txt = ''
        for value in tqdm(dictionary.values(), desc="Converting to plain text", unit="value"):
            txt += value + ' '

        return txt


if __name__ == "__main__":
    # Example usage
    file_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_posts.jsonl'
    preprocessor = JsonPreprocessor(file_path, time='afterElection')
    preprocessor.open_json_file()
    comments = preprocessor.parse_reddit_comments()

