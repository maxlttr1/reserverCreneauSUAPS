# Pas d'import de AutoSUAPS pour éviter un import circulaire
import schedule
import datetime
import pytz
import json
import os

BASE_DIR = os.path.dirname(__file__)

def readJSON() :
    with open(os.path.join(BASE_DIR, '../config/config.json'), 'r') as file :
        return list(json.load(file)["ids_resa"])

def getParisDatetime() :
    return datetime.datetime.now(pytz.timezone('Europe/Paris'))


def actions(auto) :
    auto.login()
    auto.reserverCreneau()
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


def setAllSchedules(auto):
    if(dico_activites := auto.getSchedules()) is None :
        # Fix en dur à cause des vacances
        schedule.every().tuesday.at("20:03", "Europe/Paris").do(actions, auto)
        schedule.every().thursday.at("19:33", "Europe/Paris").do(actions, auto)
    
    else : 
        for creneau in dico_activites:
            setSchedule(creneau['day'], creneau['hour'], auto)