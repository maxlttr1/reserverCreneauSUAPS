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

def readJSON() :
    with open('config.json', 'r') as file :
        return dict(json.load(file))
    
def actions(auto : AutoSUAPS) :
    auto.login()
    liste_creneaux = readJSON()["ids_resa"]
    auto.reserverCreneau(liste_creneaux)
    auto.logout()

def setSchedule(day, hour, auto) :
    match day :
        case "lundi" :
            schedule.every().monday.at(hour).do(actions, auto)
        case "mardi" :
            schedule.every().tuesday.at(hour).do(actions, auto)
        case "mercredi" :
            schedule.every().wednesday.at(hour).do(actions, auto)
        case "jeudi" :
            schedule.every().thursday.at(hour).do(actions, auto)
        case "vendredi" :
            schedule.every().friday.at(hour).do(actions, auto)
        case "samedi" :
            schedule.every().saturday.at(hour).do(actions, auto)
        case "dimanche" :
            schedule.every().sunday.at(hour).do(actions, auto)

def setAllSchedules(auto) :
    dico = readJSON()
    for day in dico["jours"] :
        for hour in dico["jours"][day] :
            setSchedule(day, hour, auto)


if __name__ == '__main__' :
    auto = AutoSUAPS(USERNAME, PASSWORD)
    setAllSchedules(auto)
    counter = 0
    old_run = datetime.datetime(1970, 1, 1)
    while datetime.datetime.now().second != 0 :
        time.sleep(1)

    while True :
        schedule.run_pending()
        
        if counter % 60 == 0 :
            next_run = schedule.next_run()
            if next_run != old_run :
                print(f"Prochaine exécution : {schedule.next_run().strftime('%d-%m-%Y %H:%M:%S')}")
                old_run = next_run
            
        time.sleep(60)
        counter += 1