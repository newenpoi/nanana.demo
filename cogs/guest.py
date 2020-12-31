import discord
from discord.ext import commands
from discord.utils import get

import re
import random

from lib import helper
from lib.db import Database
from lib.reader import Reader

r = Reader()

# TODO :
# Gérer les Erreurs SQL

class GuestCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'help')
    async def help(self, ctx, arg = None):
        """Renvoie l'aide."""
        if arg is None:
            reply = r.read('system', 'help')
        else:
            reply = r.read('help', arg)
            if not reply:
                reply = r.read('help', 'unknown')
        await ctx.send(reply)

def setup(client):
    client.add_cog(GuestCog(client))
