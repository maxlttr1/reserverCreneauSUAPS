from Fonctions import AutoSUAPS
from dotenv import load_dotenv
from os import getenv
import time

load_dotenv()

LOGIN_URL = getenv("LOGIN_URL")
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")


'''
Si vous lancez le programme pour la premiere fois, 2 solutions :
- vous voulez juste essayer une fois
- vous voulez réserver de manière récurrente

Pour la premirère solution, il vous suffit d'appeler la fonction reserverCreneau sans argument,
la fonction vous demandera un input pour savoir ce que vous voulez réserver.

Sinon, utilisez ce bout de code pour afficher les IDs des activités que vous souhaitez réserver,
et le programme pourra réserver chaque semaine

auto = AutoSUAPS(USERNAME, PASSWORD, LOGIN_URL)
auto.printIDs()

Ensuite, mettez ces IDs dans la liste ci-dessus et 
réservez-les avec : 

auto.reserverCreneau(ids_creneaux_a_resa)
'''


# 1ère solution
# auto = AutoSUAPS(USERNAME, PASSWORD, LOGIN_URL)
# auto.reserverCreneau()


# 2ème solution
ids_creneaux_a_resa = ['a67c920a-fc66-452c-8d07-5d7206a44f5b', 
                       '6ab242fa-79cd-435a-a71b-5dceb122b775',
                       '369278cd-f3e2-4432-b6b3-ca7437f11854']

while True:
    auto = AutoSUAPS(USERNAME, PASSWORD, LOGIN_URL)
    auto.reserverCreneau(ids_creneaux_a_resa)
    time.sleep(60)
    
# schedule.every().saturday.at("10:01").do(actions)
