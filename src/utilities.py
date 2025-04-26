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


def actions(auto, id) :
    auto.login()
    auto.reserverCreneau()
    auto.logout()
    

def setSchedule(id, day, hour, auto) :
    match day :
        case "lundi" :
            schedule.every().monday.at(hour, "Europe/Paris").do(actions, auto, id)
        case "mardi" :
            schedule.every().tuesday.at(hour, "Europe/Paris").do(actions, auto, id)
        case "mercredi" :
            schedule.every().wednesday.at(hour, "Europe/Paris").do(actions, auto, id)
        case "jeudi" :
            schedule.every().thursday.at(hour, "Europe/Paris").do(actions, auto, id)
        case "vendredi" :
            schedule.every().friday.at(hour, "Europe/Paris").do(actions, auto, id)
        case "samedi" :
            schedule.every().saturday.at(hour, "Europe/Paris").do(actions, auto, id)
        case "dimanche" :
            schedule.every().sunday.at(hour, "Europe/Paris").do(actions, auto, id)


def setAllSchedules(auto):
    schedule.clear()
    for creneau in auto.getSchedules() :
        setSchedule(creneau['id'], creneau['day'], creneau['hour'], auto)


def setDefaultSchedules(auto) :
    data = {"ids_resa": ["a67c920a-fc66-452c-8d07-5d7206a44f5b", "c12b09b0-8660-4b3c-9711-983317af0441", "eba1eb76-55b8-4ae4-a067-6182f3e6707b"]}
    
    with open(os.path.join(BASE_DIR, '../config/config.json'), 'w') as file :
        json.dump(data, file, indent=4)
        
    schedule.clear()
    
    schedule.every().wednesday.at("21:47", "Europe/Paris").do(actions, auto, data["ids_resa"][0])
    schedule.every().thursday.at("19:33", "Europe/Paris").do(actions, auto, data["ids_resa"][1])
    schedule.every().tuesday.at("20:03", "Europe/Paris").do(actions, auto, data["ids_resa"][2])