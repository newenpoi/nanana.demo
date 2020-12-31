import os
import discord
from discord.ext import commands

from lib import helper
from lib.db import Database
from lib.reader import Reader

from colorama import init, Fore
init(autoreset = True)

class MemberCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'ping')
    @commands.guild_only()
    async def ping(self, ctx):
        """Renvoie le temps de latence."""
        await ctx.send(f'Bwaaaaah! {round(self.client.latency)} ms.')

def setup(client):
    client.add_cog(MemberCog(client))