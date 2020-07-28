from discord.ext import commands

from digibot.conf import getDataDir
from digibot.lib import quotedb
from digibot.lib.utils import canBeInt

quotepath = getDataDir() / "quotes.sqlite3"

lastUserToSuccessfullyAddAQuote = None


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
    async def random(self, ctx, *, author = None):
        # Get a random quote, either overall or by an author.
        await ctx.send(quotedb.random(author))

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
            # Python doesn't have switch case soooooo
            if arg.startswith("before:"):
                # Set before date.
                a = arg.replace("before:", "", 1)
                before = a
                explanation += f" from before {a},"
            elif arg.startswith("after:"):
                # Set after date.
                a = arg.replace("after:", "", 1)
                after = a
                explanation += f" from after {a},"
            elif arg.startswith("author:"):
                # Append to authors.
                a = arg.replace("author:", "", 1)
                authors.append(a)
                explanation += f" by the author {a},"
            elif arg.startswith("from:"):
                a = arg.replace("from:", "", 1)
                authors.append(a)
                explanation += f" by the author {a},"
                # Set author.
                pass
            elif arg.startswith("term:"):
                # Append to terms list.
                a = arg.replace("term:", "", 1)
                terms.append(a)
                explanation += f" with the term {a},"
            elif arg.startswith("contains:"):
                # Append to terms list.
                a = arg.replace("term:", "", 1)
                terms.append(a)
                explanation += f" with the term {a},"
                pass

        # Remove last comma.
        if explanation:
            explanation = explanation[:-1]

        await ctx.send(f"Searching for quotes" + explanation + "!")
        quotelist = quotedb.advanced_search(before = before, after = after, authors = authors, terms = terms)
        q = "\n".join(str(q) for q in quotelist)
        if len(q) > 1999:
            await ctx.send(q[:1996] + "...")
        else:
            await ctx.send(q)

    @quote.command()
    async def add(self, ctx, *, s):
        # STUB
        # This is going to need to be thought about hard.
        # How do you parse the author vs. custom author?
        # How much of the formatting is up to the user?
        # How do we deal with quote marks in the strings the user inputs?

        global lastUserToSuccessfullyAddAQuote

        lastUserToSuccessfullyAddAQuote = ctx.message.author.id
        await ctx.send("This will need a lot of logic to work~!")
        quotedb.add("DigiDuncan", "Quote")

    @quote.command()
    async def remove(self, ctx, *, num):
        # STUB
        # Mod-only command.
        if canBeInt(num):
            await ctx.send("**MODS ONLY**"
                           f"Are you sure you want to remove quote {num}?\n"
                           "*[add a reaction menu here]*")
            quotedb.remove(num)

    @quote.command()
    async def undo(self, ctx):
        # STUB
        global lastUserToSuccessfullyAddAQuote

        if not lastUserToSuccessfullyAddAQuote:
            await ctx.send("Nothing to undo!")
            return
        if ctx.message.author.id == lastUserToSuccessfullyAddAQuote:
            await ctx.send(f"Are you sure you want to remove quote {quotedb.latest().iden}?\n"
                           "*[add a reaction menu here]*")
            quotedb.remove(quotedb.latest().iden)
        else:
            await ctx.send(f"Sorry, only <@!{lastUserToSuccessfullyAddAQuote} can do that.")


def setup(bot):
    bot.add_cog(QuoteCog(bot))
