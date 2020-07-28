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


def setup(bot):
    bot.add_cog(QuoteCog(bot))
