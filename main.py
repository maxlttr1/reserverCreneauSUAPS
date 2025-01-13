from Fonctions import AutoSUAPS
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

Sinon, utilisez ce bout de code pour afficher les IDs des activités que vous souhaitez réserver,
et le programme pourra réserver chaque semaine

auto = AutoSUAPS(USERNAME, PASSWORD)
auto.printIDs()

Ensuite, mettez ces IDs dans la liste ci-dessus et 
réservez-les avec : 

auto.reserverCreneau(ids_creneaux_a_resa)
'''


# 1ère solution
# auto = AutoSUAPS(USERNAME, PASSWORD) # Décommentez
# auto.printIDs() # Décommentez


# 2ème solution
ids_creneaux_a_resa = ['a67c920a-fc66-452c-8d07-5d7206a44f5b', 
                       'c12b09b0-8660-4b3c-9711-983317af0441',
                       '6ab242fa-79cd-435a-a71b-5dceb122b775']

def actions(creneaux = ids_creneaux_a_resa) :
    auto = AutoSUAPS(USERNAME, PASSWORD)
    auto.reserverCreneau(creneaux)

if __name__ == '__main__' :
    
    # Adapter selon jour & heure
    schedule.every().saturday.at("12:02").do(actions)
    schedule.every().thursday.at("19:32").do(actions)

    while True:
        schedule.run_pending()
        time.sleep(60)
    
