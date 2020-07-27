import arrow
from functools import total_ordering

from digibot.conf import getDataDir

quotepath = getDataDir() / "quotes.sqlite3"


@total_ordering
class Quote:
    def __init__(self, iden, author, text):
        self.iden = iden
        self.author = author
        self.text = text
        self.date = arrow.now()

    @property
    def year(self):
        return self.date.year

    def __lt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        return self.date == other.date
