# -*-coding: utf-8 -*-
import os
import enum
import configparser, json

'''
    Mémo:
    Fonction utile built-in de Discord.
    if discord.utils.get(message.guild.roles, name = 'Organizer'):
'''

def first(dic):
    """Retourne la première valeur non-null d'un dictionnaire."""
    return next(iter(dic.values()))

def nest(d):
    """Retourne un ou plusieurs objets imbriqués de type Structure."""
    if isinstance(d, list):
        d = [nest(x) for x in d]
    if not isinstance(d, dict):
        return d
    class Structure(object):
        pass
    objet = Structure()
    for k in d:
        objet.__dict__[k] = nest(d[k])
    return objet

def ini(field):
    """Récupère le contenu d'une section (field) d'un fichier ini et le renvoie sous forme d'objet accessible."""
    config = configparser.RawConfigParser()
    config.read(f'{os.getcwd()}/config/dev.ini')

    items = {}

    for i in range(len(config.items(field))):
        # {Clé: Valeur} (du fichier ini).
        items.update({config.options(field)[i]: config.get(field, config.options(field)[i])})
    
    return nest(items)

class ActivityType(enum.IntEnum):
    unknown = -1
    playing = 0
    streaming = 1
    listening = 2
    watching = 3