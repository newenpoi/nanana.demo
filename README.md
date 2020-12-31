## Introduction

Attention dans cette démonstration (15% de fonctionnalités) il n’y a pas de point d’entrée appelant les **listeners** (qui appellent les décorateurs si vous préférez) car cette idée je ne l’ai envisagée que récemment afin **d’organiser le code de manière efficace**.

En effet ça devient vite le chaos avec Python quand on ne fait pas attention à ses structures de données, c’est pour ça que je vous encourage donc à ne **pas nécessairement** suivre mon exemple dans le fichier main.py mais à vous étudier en priorité le **module d’extension** que vous retrouverez dans la **documentation officielle**.

Néanmoins si vous ne vous sentez pas en confiance ou que votre bot est avant tout un usage exclusif aux commandes vous pouvez garder ce schéma sans problème.

Vous avez _main.py_ d'où démarre le bot et contenant le code de base hors décorateurs de commandes qui se situent dans les **rouages** (cogs) appelés par le module d’extension Discord.

Pas mal de choses ont changé depuis la version 1.5 du module Discord donc j’ai essayé à la hâte de caser le nécessaire dans une petite démo.

**La démo a besoin des modules externes suivants :**

```
discord (pip install -U discord.py==1.5.1);
colorama (pip install colorama);
pyquery (pip install pyquery);
mysql-connector-python (pip install mysql-connector-python);
```

Ces modules nécessitent une installation manuelle via pip.

## Framework

J’ai écrit un petit module introduit dans le Framework (fichier helper/reader.py) permettant de lire le contenu d’une balise html par identifiant ou par classe pour permettre de récupérer une réponse unique ou aléatoire, vous pouvez aisément adapter le code en fonction de vos besoins.

Vous retrouverez les balises dans les fichiers html stockées dans le dossier nanana/strings.
**Ce module nécessite pyquery pour fonctionner.**

Une classe helper vous ai également proposé avec quelques fonctions d’utilités.
Vous devez spécifier votre **token** et le **canal** par défaut du bot dans le **fichier de configuration** config/dev.ini.

La fonction périodique a été spécifié en brut de s’exécuter une fois toutes les heures, celle-ci permet de synchroniser les membres du serveur avec la base de données, vous pouvez bien entendu y ajouter vos propres méthodes.

## Décorateurs

Le décorateur on_ready est suffisamment explicite et commenté pour vous laisser un aperçu.
Dans le décorateur on_message un exemple de contrôle sur le contenu est ajouté, ici on interdit la diffusion de GIF **dans un canal défini au cœur du fichier de configuration** (paramètre channel_pics), ceci reste possible même si le bot possède un canal unique, puisque seules les commandes sont affectées.

Je vous ai ajouté une regex dans le décorateur on_reaction_add afin de procéder à des interactions spécifiques pour les emoji personnalisés.

## Gestion de la Base de Données

Vous devez **modifier les paramètres du fichier de configuration** ini si vous souhaitez utiliser ce système pour **étendre les capacités dynamiques** de votre bot (section SQL du fichier config/dev.ini). Laissez le champ mot de passe vide si votre base de donnée n’en a aucun (si vous êtes en local).

En fonction du nombre de membres sur votre serveur vous risquez de voir s’affoler la console au premier lancement, ne vous inquiétiez pas, tant que vous n’avez pas d’erreurs affichés c’est que tout va bien.

**Une base de données est fournie avec la démo (nanami_demo.sql).**

Bon je sais que ce n’est pas l’affaire du siècle mais je vous ai tout de même fourni la structure avec les tables initiales de la base de données.

Celle-ci contient toutes les associations de clés primaires et étrangères dont aura besoin l’architecture pour fonctionner proprement. La gestion des tables, des fonctions et des procédures stockées revient à la responsabilité du lecteur.

J’espère que cette démo pourra vous être utile de près ou de loin, sur ce je vous souhaite un excellent réveillon !

N
