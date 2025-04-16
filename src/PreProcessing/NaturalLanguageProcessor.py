import regex as re

class NaturalLanguageProcessor:
    def __init__(self, text):
        self.text = text

    def lower(self):
        self.text = self.text.lower()

    def remove_links(self):
        self.text = re.sub(r'http\S+', '', self.text)

    def remove_stopwords(self):
        pass
