# -*-coding: utf-8 -*-
import random
import re
import mysql.connector

from lib import helper

class Database:
    """Gestion i/o de la base de données."""
    def __init__(self):
        config  = helper.ini('SQL')
        try:
            self._conn = mysql.connector.connect(
                host = config.host,
                user = config.user,
                passwd = config.password,
                database = config.db,
                autocommit = True
            )
            self._cursor = self._conn.cursor(dictionary = True)
        except:
            print(" Impossible de se connecter à la base de données.\nLes fonctionnalités seront limitées.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit = True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params = None):
        self.cursor.execute(sql, params or ())

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def ids(self):
        """Renvoie un tableau de tous les id des membres dans la base de données."""
        self.execute(f"SELECT User_ID FROM fellows")

        result = [item['User_ID'] for item in self.fetchall()]

        return result
    
    def infos(self, user_id):
        """Renvoie les informations de l'utilisateur."""
        self.execute(f"SELECT * FROM fellows WHERE User_ID = {user_id}")

        result = helper.nest(self.fetchone())

        return result

    def reg(self, user_id, user_name):
        """Enregistre l'utilisateur au sein de la base de données."""
        options = helper.ini('OPTIONS')

        user_name = re.escape(user_name)

        self.execute('''
            INSERT INTO fellows (User_ID, Name, Gold)
            VALUES (%i, "%s", %i)
            ON DUPLICATE KEY UPDATE Name = "%s"
        ''' % (user_id, user_name, int(options.gold), user_name))

    def remove(self, user_id):
        """Supprime définitivement l'utilisateur de la base de données."""
        self.execute(f"DELETE FROM Fellows WHERE User_ID = {user_id}")

    def count(self, context, user_id = None):
        """Retourne le nombre d'entrées selon le contexte souhaité."""
        if context == 'members':
            self.execute("SELECT COUNT(*) FROM fellows")
        elif context == 'inventory':
            self.execute(f"SELECT COUNT(*) FROM inventory WHERE ID_User = {user_id}")
        else:
            return False

        return helper.first(self.fetchone())