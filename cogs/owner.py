import discord
from discord.ext import commands

import re
import time

from lib.db import Database
from lib.reader import Reader

r = Reader()

class OwnerCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name = 'load', hidden = True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        '''
            Active le mécanisme d'extension.
        '''
        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Désolée, Nanana ne peut pas activer ce rouage [{cog}] car la console indique : *{type(e).__name__}*.')
        else:
            await ctx.send("Nanana vient d'activer ce rouage !")
    
    @commands.command(name = 'unload', hidden = True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        '''
            Désactive le mécanisme d'extension.
        '''
        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Désolée, Nanana ne peut pas désactiver ce rouage [{cog}] car la console indique : *{type(e).__name__}*.')
        else:
            await ctx.send('Nanana vient de désactiver ce rouage !')
    
    @commands.command(name = 'reload', hidden = True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        '''
            Recharge le mécanisme d'extension (ex: !reload cogs.owner).
        '''
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f"Désolée, Nanana ne peut pas redémarrer ce rouage [{cog}] car la console indique : *{type(e).__name__}*.")
        else:
            await ctx.send('Nanana vient de redémarrer ce rouage !')

    @commands.command(hidden = True)
    @commands.is_owner()
    async def latest(self, ctx):
        """Renvoie les dernières informations de version."""
        await ctx.send(r.read('system', 'latest'))

    @commands.command(hidden = True)
    @commands.is_owner()
    async def infos(self, ctx, member: discord.Member = None):
        """Récupère les informations de l'utilisateur."""
        with Database() as db:
            r = db.infos(member.id)
            await ctx.send(f" Pseudo : x ; Identifiant : {r.ID}.")

def setup(client):
    client.add_cog(OwnerCog(client))