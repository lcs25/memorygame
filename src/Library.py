import random
from pathlib import Path

from src.helpers.text_parsing import get_text

class Library:
    def __init__(self, location):
        self.location = location
        self.books = {}
        self.load()

    def load(self):
        folder_path = Path(self.location)
        files = [f for f in folder_path.iterdir() if f.is_file()]
        for f in files:
            content = get_text(f)
            self.books[str(f)] = content

    def get_random_sentences(self, count):
        sentences = []
        books = list(self.books.keys())
        i = 0
        while len(sentences) < count:
            title = books[i]
            s = self.get_random_sentence(title)
            sentences.append(s)
            i += 1
            if i == len(books):
                i = 0
        return sentences

    def get_random_sentence(self, title=None):
        if not title:
            dkeys = self.books.keys()
            rd = random.randrange(0, len(dkeys)-1)
            title = dkeys[rd]
        text = self.books[title]
        rd = random.randrange(0, len(text))
        return text[rd]