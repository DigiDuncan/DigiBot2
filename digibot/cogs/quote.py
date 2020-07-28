from discord.ext import commands

from digibot.conf import getDataDir
from digibot.lib import quotedb
from digibot.lib.utils import canBeInt

quotepath = getDataDir() / "quotes.sqlite3"


class QuoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            # Get quote by ID.
            num = ctx.subcommand_passed
            if num and canBeInt(num):
                await ctx.send(f"Loading quote {num}...")
                await ctx.send(quotedb.getQuoteByID(num))
            else:
                await ctx.send(f"Invalid quote or subcommand {num}.")

    @quote.command()
    async def search(self, ctx, *, term):
        # Search quotes by a search term in the text of the quote.
        await ctx.send(f"Searching for quotes containing {term}...")
        quotelist = quotedb.search(term)
        q = "\n".join(str(q) for q in quotelist)
        if len(q) > 1999:
            await ctx.send(q[:1996] + "...")
        else:
            await ctx.send(q)

    @quote.command()
    async def latest(self, ctx, *, author = None):
        # Get the latest quote, either overall or by an author.
        await ctx.send(quotedb.latest(author))

    @quote.command()
    async def advsearch(self, ctx, *, s):
        # Filters.
        before = None
        after = None
        authors = []
        terms = []
        explanation = ""

        args = s.split()
        for arg in args:
            if arg.startswith("before:"):
                # Set before date.
                a = arg.replace("before:", "", 1)
                before = a
                explanation += f" from before {a},"
            if arg.startswith("after:"):
                # Set after date.
                a = arg.replace("after:", "", 1)
                after = a
                explanation += f" from after {a},"
            if arg.startswith("author:"):
                # Append to authors.
                a = arg.replace("author:", "", 1)
                authors.append(a)
                explanation += f" by the author {a},"
            if arg.startswith("from:"):
                a = arg.replace("from:", "", 1)
                authors.append(a)
                explanation += f" by the author {a},"
                # Set author.
                pass
            if arg.startswith("term:"):
                # Append to terms list.
                a = arg.replace("term:", "", 1)
                terms.append(a)
                explanation += f" with the term {a},"
            if arg.startswith("contains:"):
                # Append to terms list.
                a = arg.replace("term:", "", 1)
                terms.append(a)
                explanation += f" with the term {a},"
                pass

        if explanation:
            explanation = explanation[:-1]

        await ctx.send(f"Searching for quotes" + explanation + "!")
        quotelist = quotedb.advanced_search(before = before, after = after, authors = authors, terms = terms)
        q = "\n".join(str(q) for q in quotelist)
        if len(q) > 1999:
            await ctx.send(q[:1996] + "...")
        else:
            await ctx.send(q)


def setup(bot):
    bot.add_cog(QuoteCog(bot))
