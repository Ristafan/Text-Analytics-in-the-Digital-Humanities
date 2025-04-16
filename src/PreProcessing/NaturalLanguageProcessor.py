import regex as re
from stop_words import get_stop_words


class NaturalLanguageProcessor:
    def __init__(self, text):
        self.text = text

    def lower(self):
        self.text = self.text.lower()

    def remove_links(self):
        self.text = re.sub(r'http\S+', '', self.text)

    def remove_stopwords(self):
        stop_words = get_stop_words('english')
        for word in self.text.split():
            if word in stop_words:
                self.text = re.sub(word, '', self.text)
