# -*-coding: utf-8 -*-
'''
    Nanana
    Démonstration

    Last Updated:
    30/12/20
'''

import asyncio
import time
import random
import re

import discord

# Extensions
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Framework
from lib import helper
from lib.db import Database
from lib.reader import Reader

# Classes
from colorama import init, Fore
init(autoreset = True)

# Paramètrages :
config  = helper.ini('SYSTEM')
initial_extensions = ['cogs.owner', 'cogs.member', 'cogs.guest']

# Global
db = Database()
r = Reader()

# Discord Python >= 1.5.0
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command('help')

if __name__ == '__main__':
    # Ce scope s'execute en premier et évite de lancer le bot en cas d'une mauvaise configuration.
    if config.token == '0':
        print(Fore.RED + "Le token de votre api (discord.com/developers) n'a pas été spécifié. Vérifiez le fichier de configuration à l'emplacement suivant : config/dev.ini et relancez l'application.\n")
        exit(1)

    if config.channel_bot == '0':
        print(Fore.RED + "Le canal par défaut du bot n'a pas été spécifié. Vérifiez le fichier de configuration à l'emplacement suivant : config/dev.ini et relancez l'application.\n")
        exit(1)
        
    for extension in initial_extensions:
        client.load_extension(extension)

async def periodic(channel, sv_members, timer):
    """
        Fonction asynchrone périodique.
    """
    while True:
        print(Fore.CYAN + "\n Vérification périodique...\n")

        with Database() as db:
            # Récupère l'identifiant des membres de la db et de la guilde (serveur).
            db_ids = db.ids()
            sv_ids = [member.id for member in sv_members]

            # TODO: Préférable lors des maintenances.
            # Supprime le membre de la base de données s'il n'est plus présent sur le serveur.
            for sv_id in db_ids:
                if not sv_id in sv_ids:
                    db.remove(sv_id)

            # Synchronisation si le nombre d'utilisateurs dans la base de données est inférieur à celui du serveur.
            if db.count('members') < len(sv_members):
                print(Fore.CYAN + " Synchronisation en cours, veuillez patienter...\n")
                for member in sv_members:
                    if member.id not in db_ids:
                        print(f' Synchronisation du membre : {member.id} avec pour pseudo {member.display_name}...')
                        db.reg(member.id, member.display_name)
        # Dodo.
        await asyncio.sleep(timer)

@client.event
async def on_ready():
    """Décorateur d'initialisation du Bot."""
    guilds = []
    
    # Récupère les serveurs dans lequel le bot se trouve.
    for guild in client.guilds:
        guilds.append(guild)
    
    # Récupère un channel exclusif pour le bot.
    channel = client.get_channel(int(config.channel_bot))

    print(Fore.GREEN + f' {client.user} connecté avec succès au(x) serveur(s) :\n')

    for guild in guilds:
        print(f'{Fore.YELLOW} {guild.name}.')

    # Affiche les membres du premier serveur (celui qui nous intéresse).
    members = '\n - '.join([member.name for member in guilds[0].members])
    print(f'\n Membres :\n - {members}')
    
    # Message de connexion.
    await channel.send(r.read('system', 'greetings'))

    # Activité.
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = 'les Rouages du Renouveau', type = helper.ActivityType.listening))
    
    # Async périodique.
    await asyncio.create_task(periodic(channel, guilds[0].members, 3600))

@client.event
async def on_message(message):
    """Décorateur en cas de réception de message et appel à la coroutine."""
    if message.author == client.user:
        return

    # Empêche la diffusion de GIF dans le canal spécifié depuis la configuration.
    if message.channel.id == int(config.channel_pics):
        try:
            if message.attachments[0].url.lower().endswith('gif'):
                await message.channel.send(r.read('system', 'no-gif-channel'))
                await message.delete()
        except IndexError:
            pass
        
    # Doit appeler la coroutine process_commands en cas de réecriture on_message.
    if message.channel.id == int(config.channel_bot) or isinstance(message.channel, discord.DMChannel):
        await client.process_commands(message)

@client.event
async def on_member_join(member):
    """Décorateur pour l'accueil d'un nouvel utilisateur."""
    await member.create_dm()
    # Vous n'êtes pas obligés de passer par la classe Reader vous pouvez tout simplement formatter votre réponse comme bon vous semble.
    await member.dm_channel.send(f'Yaa-hoo ! Nanana est là si tu as besoin de quelque chose !')

@client.event
async def on_reaction_add(reaction, user):
    """
        Décorateur en cas de réaction.
        Vous pouvez adapter cette partie en fonction de vos besoins.
    """
    print(f" On a réagis à un message de {Fore.MAGENTA}Nanana{Fore.WHITE} !")

    # Récupération du titre de la réaction (si réaction personnalisée).
    try:
        string = re.search(r'^.*\:(.*)\:.*$', str(reaction)).group(1)
    except:
        # On a plus rien à faire ici.
        return
    else:
        # Vérifions que cette réaction est celle qu'on attend et qu'on ne réagis pas à notre propre réaction.
        if string in ['emoji_custom_a', 'fight'] and reaction.message.author.name is not user.name:
            print(f' {user.name} aimerait en découdre waaaaah !')

@client.event
async def on_command_error(ctx, error):
    """Décorateur en cas de commande erronée."""
    if isinstance(error, CommandNotFound):
        return
    raise error

# Démarrage du Bot.
client.run(config.token)