import json
from flask import Flask, render_template, request, redirect, url_for

from Fonctions import *
from dotenv import load_dotenv
from os import getenv
import time
import schedule
import os

BASE_DIR = os.path.dirname(__file__)

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../config/.env'), override=True)
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

app = Flask(__name__)

def read_config():
    with open('../config/config.json', 'r') as config_file:
        return json.load(config_file)

def save_config(config):
    with open('../config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

from flask import Flask, render_template

@app.route('/')
def home():
    auto = AutoSUAPS(USERNAME, PASSWORD)
    auto.login()

    config_file = read_config()

    df = auto.getActivitiesInfo()
    activities_dict = df.to_dict(orient='records')
    print(activities_dict)

    auto.logout()
    return render_template('index.html', config_file=config_file, activities_dict = activities_dict)

@app.route('/update', methods=['POST'])
def update():
    config_file = read_config()

    for day in config_file["jours"]:
        new_times = request.form.get(day)
        if new_times:
            config_file["jours"][day] = [time.strip() for time in new_times.split(',')]
        else:
            config_file["jours"][day] = []

    save_config(config_file)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
