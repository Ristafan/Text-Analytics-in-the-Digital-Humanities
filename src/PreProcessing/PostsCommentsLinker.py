import os
import json
from tqdm import tqdm


class PostsCommentsLinker:
    def __init__(self, posts_path, comments_path):
        self.posts_path = posts_path
        self.comments_path = comments_path
        self.post_ids = {}  # Use a dictionary to store post IDs (without the 't3_' prefix)
        self.linked_data = {}

    def open_json_file(self, path):
        assert os.path.exists(path), f'Path to file is incorrect: {path}'
        with open(path, 'r', encoding="utf8") as json_file:
            return list(json_file)

    def get_post_ids(self):
        posts_list = self.open_json_file(self.posts_path)
        for json_str in tqdm(posts_list, desc="Parsing posts", unit="post"):
            obj = json.loads(json_str)
            post_id = obj['name'].replace('t3_', '')  # Extract post ID without 't3_'
            self.post_ids[post_id] = obj['title'] + " " + obj['selftext']
            self.linked_data[post_id] = obj['title'] + " " + obj['selftext'] + " " # Initialize linked data with post content

    def link_comment_ids_to_post_ids(self):
        comments_list = self.open_json_file(self.comments_path)
        for json_str in tqdm(comments_list, desc="Parsing comments", unit="comment"):
            obj = json.loads(json_str)
            link_id_without_prefix = obj['link_id'].replace('t3_', '') # Remove 't3_' prefix from link_id
            if link_id_without_prefix in self.post_ids:
                # print(f'Found post id: {link_id_without_prefix} and comment id: {obj["name"]}')
                self.linked_data[link_id_without_prefix] += obj['body'] + " "

    def save_linked_data(self, output_path):
        with open(output_path, 'w', encoding="utf8") as json_file:
            json.dump(self.linked_data, json_file, ensure_ascii=False, indent=4)

    def link_comments_to_posts(self):
        self.get_post_ids()
        self.link_comment_ids_to_post_ids()


if __name__ == '__main__':
    posts_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_posts(beforeElection).jsonl'
    comments_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/r_MensRights_comments(beforeElection).jsonl'
    output_path = 'C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/reddit/MensRights/MensRights(before)_linked_data.json'

    linker = PostsCommentsLinker(posts_path, comments_path)
    linker.link_comments_to_posts()
    linker.save_linked_data(output_path)