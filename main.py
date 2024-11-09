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
ids_creneaux_a_resa = ['a67c920a-fc66-452c-8d07-5d7206a44f5b', 
                       '6ab242fa-79cd-435a-a71b-5dceb122b775',
                       '369278cd-f3e2-4432-b6b3-ca7437f11854']

'''auto = AutoSUAPS(USERNAME, PASSWORD, LOGIN_URL)
# Si la liste creneaux_a_resa en arg, rien à faire. Si pas d'arg, on prend l'input utilisateur.
auto.reserverCreneau(ids_creneaux_a_resa)'''

print('online')

import schedule
import time
def actions() :
    auto = AutoSUAPS(USERNAME, PASSWORD, LOGIN_URL)
    auto.reserverCreneau(ids_creneaux_a_resa)
    
schedule.every().saturday.at("10:01").do(actions)

while True:
    schedule.run_pending()
    time.sleep(1)
