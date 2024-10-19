from Fonctions import AutoSUAPS
from dotenv import load_dotenv
from os import getenv

load_dotenv()

LOGIN_URL = getenv("LOGIN_URL")
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

'''Dans cette liste, rentrez : 
-> le nom de l'activité (ou juste le début, par ex. ju-jitsu suffit, pas la peine de mettre le nom complet)
-> le jour exact
-> la date de DÉBUT de l'activité, ça suffit
'''
creneaux_a_resa = ['ju-jitsu lundi 17:30',
                   'escalade mardi 18:00']

auto = AutoSUAPS(USERNAME, PASSWORD, LOGIN_URL)

# Si la liste creneaux_a_resa en arg, rien à faire. Si pas d'arg, on prend l'input utilisateur.
auto.reserverCreneau()
