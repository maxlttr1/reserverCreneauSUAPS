import json
from flask import Flask, render_template, request, redirect, url_for

#Créer une instance
app = Flask(__name__)

def read_config():
    with open('../config/config.json', 'r') as config_file:
        return json.load(config_file)

def save_config(config):
    with open('../config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

from flask import Flask, render_template

#Route vers la home page
@app.route('/')
def home():
    config_file = read_config()

    config = {
        "ids_resa": [
            "a67c920a-fc66-452c-8d07-5d7206a44f5b", 
            "c12b09b0-8660-4b3c-9711-983317af0441", 
            "eba1eb76-55b8-4ae4-a067-6182f3e6707b"
        ],
        "jours": {
            "lundi": [],
            "mardi": ["20:01"],
            "mercredi": [],
            "jeudi": ["19:31"],
            "vendredi": [],
            "samedi": [],
            "dimanche": []
        }
    }
    app.logger.info(config_file)

    return render_template('index.html', config_file=config_file)

if __name__ == '__main__':
    app.run(debug=True)
