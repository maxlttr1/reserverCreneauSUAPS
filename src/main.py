from Fonctions import *
from dotenv import load_dotenv
from os import getenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'), override=True)
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

if __name__ == '__main__' :
    auto = AutoSUAPS(USERNAME, PASSWORD)
    auto.login()

    # Afficher les IDs des créneaux (pour reporter dans config.json)
    auto.printIDs()

    # Tester en faisant une réservation (prend un input dans le terminal)
    # auto.reserverCreneau()