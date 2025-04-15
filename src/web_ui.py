import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from AutoSUAPS import *
from utilities import setAllSchedules
from dotenv import load_dotenv
from os import getenv
import time
import os

BASE_DIR = os.path.dirname(__file__)

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../config/.env'), override=True)
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect if not logged in

activities_cache = None
activities_cache_timestamp = 0
CACHE_EXPIRATION_TIME = 600 # Time in seconds

def read_config():
    with open(os.path.join(BASE_DIR, '../config/config.json'), 'r') as config_file:
        return json.load(config_file)

def save_config(config):
    with open(os.path.join(BASE_DIR, '../config/config.json'), 'w') as config_file:
        json.dump(config, config_file, indent=4)

def get_activities():
    global activities_cache, activities_cache_timestamp
    current_time = time.time()

    if activities_cache is None or (current_time - activities_cache_timestamp) > CACHE_EXPIRATION_TIME:
        auto = AutoSUAPS(USERNAME, PASSWORD)
        auto.login()
        df = auto.getActivitiesInfo()
        activities_cache = df.to_dict(orient='records')
        activities_cache_timestamp = current_time
        auto.logout()

    return activities_cache

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        want_remember = 'remember' in request.form

        if password == PASSWORD:
            user = User("admin")
            login_user(user, remember=want_remember)
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    activities_dict = get_activities()
    config_file = read_config()

    return render_template('index.html', activities_dict = activities_dict, config_file = config_file)

@app.route('/update', methods=['POST'])
@login_required
def update():
    action = request.form.get('action')
    auto = AutoSUAPS(USERNAME, PASSWORD)
    auto.login()

    if action == 'sauvegarder':

        selected_ids = request.form.getlist('id_resa')

        if selected_ids:
            save_config({"ids_resa": list(selected_ids)})
        else:
            save_config({"ids_resa": []})

        setAllSchedules(auto)
        flash('Modifications enregistrées !')
        auto.logout()
        return redirect(url_for('home'))

    elif action == 'default':
        setDefaultSchedules(auto)
        flash('Default ok !')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)