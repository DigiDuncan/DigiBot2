import arrow
from functools import total_ordering

from digibot.lib.utils import canBeInt


@total_ordering
class Quote:
    def __init__(self, authors, text, iden = None, custom_author = None):
        self.iden = iden
        self._authors = authors
        self.text = text
        self.date = arrow.now()
        self.custom_author = custom_author

    @property
    def author(self):
        return self.custom_author or ",".join(self._authors)

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
        return f"**Quote {self.iden}:** {self.text} *-- {self.author}, {self.year}*"


def getQuoteByID(iden):
    # STUB
    return Quote(["DigiDuncan"], f"\"I hate coding and I'm quote number {iden}!\"", iden = iden)


def search(term):
    # STUB
    if canBeInt(term):
        return [Quote(["DigiDuncan"], f"\"I hate coding and you searched for {term}!\"", iden = 1)] * int(term)
    else:
        return []


def advanced_search(before = None, after = None, authors = None, terms = None):
    return [Quote(["DigiDuncan"], f"\"I hate coding and you searched for a quote from before {before}, after {after}, by {authors}, containing {terms}!", iden = 1)]


def latest(author = None):
    # STUB
    if author:
        return Quote([author], f"\"I hate coding and I'm the latest quote by {author}!\"", iden = 1000)
    return Quote(["DigiDuncan"], f"\"I hate coding and I'm the latest quote!\"", iden = 1000)


def add(author, text, custom_author = None):
    # STUB
    return Quote([author], text, custom_author=custom_author)


def remove(iden):
    # STUB
    return iden


def randomquote(author = None):
    # STUB
    if author:
        return Quote([author], f"\"I hate coding and I'm a random quote by {author}!\"", iden = 999)
    return Quote(["DigiDuncan"], f"\"I hate coding and I'm a random quote!\"", iden = 999)


def addtag(iden, tag):
    return f"Added tag `{tag}` to quote {iden}"


def removetag(iden, tag):
    return f"Removed tag `{tag}` from quote {iden}"


def listtags(iden):
    return ["tag1", "tag2", "tag3", "tag4"]
