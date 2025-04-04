from AutoSUAPS import AutoSUAPS
from utilities import setAllSchedules, getParisDatetime, actions
from dotenv import load_dotenv
from os import getenv
import os
import datetime
import schedule
import time
import pytz

BASE_DIR = os.path.dirname(__file__)

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../config/.env'), override=True)
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")


if __name__ == '__main__' :
    auto = AutoSUAPS(USERNAME, PASSWORD)
    
    auto.login()
    auto.printIDs()
    auto.logout()

    setAllSchedules(auto)
    
    # Fix en dur à cause des vacances
    schedule.every().tuesday.at("20:03", "Europe/Paris").do(actions, auto)
    schedule.every().thursday.at("19:33", "Europe/Paris").do(actions, auto)
    
    # Pour que les schedule commencent à 0 secondes pile !
    counter = 0
    old_run = datetime.datetime(1970, 1, 1)
    while getParisDatetime().second != 0 :
        time.sleep(1)

    while True :
        schedule.run_pending()
        
        if counter % 10 == 0 :
            next_run = schedule.next_run()
            if next_run and next_run != old_run :
                print(f"Prochaine exécution : {next_run.astimezone(pytz.timezone('Europe/Paris')).strftime('%d-%m-%Y %H:%M:%S')}")
                old_run = next_run
            
        time.sleep(60)
        counter += 1