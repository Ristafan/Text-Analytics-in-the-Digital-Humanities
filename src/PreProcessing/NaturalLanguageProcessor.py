import regex as re
from stop_words import get_stop_words
from tqdm import tqdm


def create_stop_words_file():
    stop_words = get_stop_words('english')
    with open('stopwords.txt', 'w', encoding='utf-8') as file:
        for word in stop_words:
            file.write(word + '\n')


class NaturalLanguageProcessor:
    def __init__(self, text, lower=True, remove_links=True, remove_stopwords=True, remove_reddit_formatting=True, remove_stars=True, remove_punctuations=True, remove_emojis=True):
        self.text = text
        self.methods_bool = [lower, remove_links, remove_stopwords, remove_reddit_formatting, remove_stars, remove_punctuations, remove_emojis]
        self.methods = [self.lower, self.remove_links, self.remove_stopwords, self.remove_reddit_formatting, self.remove_stars, self.remove_punctuations, self.remove_emojis]

        for i in range(len(self.methods)):
            if self.methods_bool[i]:
                print(self.text)
                self.methods[i]()

    def save_txt(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.text)

    def lower(self):
        self.text = self.text.lower()

    def remove_links(self):
        self.text = re.sub(r'http\S+', '', self.text)

    def remove_stopwords(self):
        stop_words = []
        # PreProcessing/stopwords.txt
        with open('stopwords.txt', 'r', encoding='utf-8') as file:
            for word in file.readlines():
                stop_words.append(word.strip())

        words = self.text.split()
        filtered_words = [word for word in words if word not in stop_words]
        self.text = ' '.join(filtered_words)

    def remove_reddit_formatting(self):
        self.text = re.sub(r'\*', '', self.text)  # bold text

    def remove_stars(self):  # often stars are used for bold formatting
        self.text = self.text.replace('*', '')

    def remove_punctuations(self):
        self.text = re.sub(r'[^\w\s]', '', self.text)

    def remove_emojis(self):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        self.text = re.sub(emoj, '', str(self.text))
        self.text = ' '.join(self.text.split())


if __name__ == "__main__":
    # Example usage
    text = "This is a **sample** text* * *with ;a ] link http://example.com and some \" $stop words ✍ 😉🌷 📌 👈🏻 🖥."
    nlp = NaturalLanguageProcessor(text)
    print()
    print(text)
    print(nlp.text)
