from Fonctions import *
from dotenv import load_dotenv
from os import getenv
import time
import schedule

load_dotenv()
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

'''
Si vous lancez le programme pour la premiere fois, 2 solutions :
- vous voulez juste essayer une fois
- vous voulez réserver de manière récurrente

Pour la première solution, il vous suffit d'appeler la fonction reserverCreneau sans argument,
la fonction vous demandera un input pour savoir ce que vous voulez réserver.

Si vous voulez réserver de manière récurrente, allez modifier le fichier config.json, en mettant dedans
les IDs des créneaux souhaités. Pour ce faire, lancez ceci :

AutoSUAPS(USERNAME, PASSWORD).printIDs()

Cela renverra tous les créneaux et leurs IDs. Puis, spécifiez les jours et heures d'exécution :)
'''

def actions(liste_creneaux = readJSON()["ids_resa"]) :
    auto = AutoSUAPS(USERNAME, PASSWORD)
    auto.reserverCreneau(liste_creneaux)
    auto.logout()


if __name__ == '__main__' :
    setAllSchedules(actions)

    while True:
        schedule.run_pending()
        time.sleep(60)