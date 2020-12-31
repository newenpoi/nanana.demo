from pyquery import PyQuery
# from multipledispatch import dispatch

import random

class Reader:
    '''Gère le flux entrée / sortie notamment des fichiers de réponses utilisateurs.'''
    _stream = None

    @property
    def stream(self):
        return type(self)._stream

    @stream.setter
    def stream(self, val):
        type(self)._stream = val

    def close(self):
        print(" Fermeture d'un accès i/o.")
        self.stream.close()

    def read(self, file, line, *args):
        """
            Lis la partie demandée (line = id) d'un fichier HTML.\n
            Les arguments sont passés via *args pour le formatage.
        """
        with open(f"./strings/{file}.html", 'r', encoding = 'utf-8') as file:
            q = PyQuery(file.read())
            tag = q(f'div#{line}')

            return tag.text(squash_space = False).format(*args)

    def rand(self, file, line, *args):
        """Lis le fichier HTML avec la classe spécifiée (line) et renvoie une réponse aléatoire."""
        with open(f"./strings/{file}.html", 'r', encoding = 'utf-8') as file:
            query = PyQuery(file.read())
            
            # Récupère le nombre de blocs contenant la classe spécifiée.
            length = len(query(f'div.{line}'))
            r = random.randint(0, length - 1)
            
            # Sélectionne un bloc random.
            tag = query(f'div.{line}').eq(r)

            # tag = query(f'.{line}#{r}') # Tester les performances avant d'employer cette méthode.
            
            return tag.text(squash_space = False).format(*args)