from Fonctions import *
from dotenv import load_dotenv
from os import getenv
import time
import schedule
import os

load_dotenv()
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

def readJSON() :
    for root, dirs, files in os.walk('.'):
        # Afficher le répertoire courant
        print(f"Répertoire : {root}")
        # Afficher les sous-répertoires
        for dir_name in dirs:
            print(f"  Sous-répertoire : {dir_name}")
        # Afficher les fichiers dans le répertoire courant
        for file_name in files:
            print(f"  Fichier : {file_name}")
            
    with open('../config/config.json', 'r') as file :
        return dict(json.load(file))
    
def actions(auto : AutoSUAPS) :
    auto.login()
    liste_creneaux = readJSON()["ids_resa"]
    auto.reserverCreneau(liste_creneaux)
    auto.logout()

def setSchedule(day, hour, auto) :
    match day :
        case "lundi" :
            schedule.every().monday.at(hour, "Europe/Paris").do(actions, auto)
        case "mardi" :
            schedule.every().tuesday.at(hour, "Europe/Paris").do(actions, auto)
        case "mercredi" :
            schedule.every().wednesday.at(hour, "Europe/Paris").do(actions, auto)
        case "jeudi" :
            schedule.every().thursday.at(hour, "Europe/Paris").do(actions, auto)
        case "vendredi" :
            schedule.every().friday.at(hour, "Europe/Paris").do(actions, auto)
        case "samedi" :
            schedule.every().saturday.at(hour, "Europe/Paris").do(actions, auto)
        case "dimanche" :
            schedule.every().sunday.at(hour, "Europe/Paris").do(actions, auto)

def setAllSchedules(auto) :
    dico = readJSON()
    for day in dico["jours"] :
        for hour in dico["jours"][day] :
            setSchedule(day, hour, auto)


if __name__ == '__main__' :
    auto = AutoSUAPS(USERNAME, PASSWORD)
    
    auto.login()
    auto.printIDs()
    auto.logout()

    setAllSchedules(auto)
    counter = 0
    old_run = datetime.datetime(1970, 1, 1)
    while getParisDatetime().second != 0 :
        time.sleep(1)

    while True :
        schedule.run_pending()
        
        if counter % 10 == 0 :
            next_run = schedule.next_run()
            if next_run != old_run :
                print(f"Prochaine exécution : {next_run.astimezone(pytz.timezone('Europe/Paris')).strftime('%d-%m-%Y %H:%M:%S')}")
                old_run = next_run
            
        time.sleep(60)
        counter += 1