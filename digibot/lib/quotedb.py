import arrow
from functools import total_ordering

from digibot.lib.utils import canBeInt


@total_ordering
class Quote:
    def __init__(self, iden, author, text, customauthor = None):
        self.iden = iden
        self._author = author
        self.text = text
        self.date = arrow.now()
        self.customauthor = customauthor

    @property
    def author(self):
        return self.customauthor or self._author

    @property
    def formatteddate(self):
        return self.date.format("YYYY-MM-DD")

    @property
    def year(self):
        return self.date.year

    def __lt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        return self.date == other.date

    def __str__(self):
        return f"{self.text} *-- {self.author}, {self.year}*"


def getQuoteByID(iden):
    # STUB
    return Quote(iden, "DigiDuncan", f"\"I hate coding and I'm quote number {iden}!\"")


def search(term):
    # STUB
    if canBeInt(term):
        return [Quote(1, "DigiDuncan", f"\"I hate coding and you searched for {term}!\"")] * int(term)
    else:
        return []


def latest(author = None):
    # STUB
    if author:
        return Quote(1, author, f"\"I hate coding and I'm the latest quote by {author}!\"")
    return Quote(1, "DigiDuncan", f"\"I hate coding and I'm the latest quote!\"")
