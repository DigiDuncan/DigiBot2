import sqlite3

import arrow
from functools import total_ordering

from digibot.conf import getDataDir
from digibot.lib.utils import canBeInt, sentence_join, NEWLINE

conn = None


def init():
    global conn
    path = getDataDir() / "quotedb.sqlite3"
    conn = sqlite3.connect(path)


class SafeCursor:
    def __init__(self, connection):
        self.con = connection

    def __enter__(self):
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, typ, value, traceback):
        self.cursor.close()


@total_ordering
class Quote:
    def __init__(self, *, authors, text, date = arrow.now(), year_only = False,
                 iden = None, custom_author = None, tags = []):
        self.iden = iden
        self._authors = authors
        self.text = text
        self.date = arrow.get(date)
        self.year_only = bool(year_only)
        self.custom_author = custom_author
        self.tags = tags

    @property
    def author(self):
        return self.custom_author or sentence_join(self._authors)

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
        return (f"**Quote {self.iden}:**{NEWLINE if ';' in self.text else ' '}"
                f"{self.text} *-- {self.author}, {self.year}*".replace(";", "\n"))

    def __repr__(self):
        return (
            f"Quote ID: {self.iden}\n"
            f"Quote Text: {self.text}\n"
            f"Quote Authors: {', '.join(self._authors)}\n"
            f"Custom Author: {self.custom_author}\n"
            f"Quote Date: {self.date if not self.year_only else self.date.year}\n"
            f"Year Only?: {self.year_only}\n"
            f"Quote Tags: {', '.join(self.tags)}"
        )

    def toSQL(self):
        return "Ha, you thought this was SQL!"


def getQuoteByID(iden):
    # STUB
    r"""SELECT ID, Quote, Date, YearOnly, CustomAuthor FROM Quotes
    WHERE ID = 521;
    SELECT ID, Name FROM QuoteAuthors
    INNER JOIN Authors ON QuoteAuthors.AuthorID = Authors.ID
    WHERE QuoteID = 521;
    SELECT ID, Name FROM QuoteTags
    INNER JOIN Tags ON QuoteTags.TagID = Tags.ID
    WHERE QuoteID = 521;"""
    with conn:
        with SafeCursor(conn) as c:
            c = conn.execute("SELECT ID, Quote, Date, YearOnly, CustomAuthor FROM Quotes WHERE ID = ?",
                             (iden, ))
            data = c.fetchone()
            if data is None:
                return None
            quoteID, text, date, year_only, custom_author = data
            c = conn.execute("SELECT Name FROM QuoteAuthors "
                             "INNER JOIN Authors ON QuoteAuthors.AuthorID = Authors.ID WHERE QuoteID = ?",
                             (iden, ))
            authors = [a[0] for a in c.fetchall()]
            c = conn.execute("SELECT Name FROM QuoteTags "
                             "INNER JOIN Tags ON QuoteTags.TagID = Tags.ID WHERE QuoteID = ?",
                             (iden, ))
            tags = [t[0] for t in c.fetchall()]

    return Quote(iden = quoteID, authors = authors, tags = tags, text = text, date = date,
                 year_only = year_only, custom_author = custom_author)


def updateQuote(iden):
    # STUB
    pass


def search(term):
    # STUB
    if canBeInt(term):
        return [Quote(["DigiDuncan"], f"\"I hate coding and you searched for {term}!\"", iden = 1)] * int(term)
    else:
        return []


def advanced_search(before = None, after = None, authors = None, terms = None):
    # STUB
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
