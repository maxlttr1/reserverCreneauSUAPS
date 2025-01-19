import datetime
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import schedule

class AutoSUAPS :
    def __init__(self, username, password, LOGIN_URL = 'https://cas6n.univ-nantes.fr/esup-cas-server/login?service=https%3A%2F%2Fu-sport.univ-nantes.fr%2Fcas%2F') :
        '''Permet de gérer les réservations de créneaux pour le SUAPS
        @param username: identifiant de l'université
        @param password: mot de passe
        @param LOGIN_URL: url de login
        '''
        self.username = username
        self.password = password
        self.session = requests.Session()
        
        # On se connecte et on set l'id de la période en cours (pour économiser des requêtes)
        self.login_csa6(LOGIN_URL)
        # self.setIDPeriode() 
        # Fix : "tkt", plus simple comme ça
        self.id_periode = 'bcb3698e-015d-4577-858b-c4cb646ea7a6'

    def login_csa6(self, LOGIN_URL) -> None :
        '''
        Permet de se connecter à son compte de l'université avec son username et password.
        
        Paramètres :
        - LOGIN_URL : URL à rejoindre pour envoyer la requête
        '''
        r = self.session.get(LOGIN_URL)

        page_login = BeautifulSoup(r.text, 'html.parser')
        inputs : list = page_login.find(id='fm1').find_all('input')

        login_data = {}
        for dico_input in inputs :
            if dico_input.attrs.get('value') is not None :
                login_data[dico_input['name']] = dico_input['value']
        login_data["username"] = self.username
        login_data["password"] = self.password

        self.session.post(r.url, login_data)

    def getEtudiant(self) -> str :
        '''
        Retourne la data JSON de l'étudiant en question (de toi qui lis ce code)
        '''
        return self.session.get('https://u-sport.univ-nantes.fr/api/individus/me').json()
        
    
    def getCreneau(self, id_creneau, id_activite) -> str | None:
        '''
        Retourne les data JSON d'un créneau à partir de son ID et de l'ID de l'activité
        '''
        URL = f'https://u-sport.univ-nantes.fr/api/extended/creneau-recurrents/semaine?idActivite={id_activite}&idPeriode={self.id_periode}&idIndividu={self.username}'
        rep = self.session.get(URL).json()
        
        for creneau in rep :
            if creneau['id'] == id_creneau :
                return creneau
        return None

    def setIDPeriode(self) -> str :
        '''
        Fait une requête pour savoir quel catalogue utiliser, selon la date actuelle. 
        Il semblerait qu'il y ait deux catalogues, le premier étant celui utilisé quasi tout le temps, et un autre
        qui est utilisé pendant 1 semaine à Noël.
        '''
        rep = self.session.get('https://u-sport.univ-nantes.fr/api/extended/periodes/catalogue?idCatalogue=')
        
        if not isinstance(rep.json(), list) :
            self.id_periode = rep.json()['id']

        else :
            todayDate = datetime.datetime.today()
            dates = {}
            for periode in rep.json() :
                id = periode['id']
                startDate = datetime.datetime.strptime(periode['dateDebutActivites'], '%Y-%m-%d')
                endDate = datetime.datetime.strptime(periode['dateFinActivites'], '%Y-%m-%d')
                dates[id] = [startDate, endDate]
            
            closest_key = list(dates.keys())[0]
            
            # Pour savoir la tranche de dates la plus rapprochée de la date actuelle
            for key, slice_date in dates.items() :
                if (slice_date[0] <= todayDate <= slice_date[1] and
                dates[closest_key][0] < slice_date[0] and
                dates[closest_key][1] > slice_date[1]) :
                    closest_key = key
            
            self.id_periode = closest_key
        
                    
    def getActivities(self) -> list[str] :
        '''
        Renvoie une liste contenant les IDs des activités de l'user (3 max)
        '''
        url_3sports = f'https://u-sport.univ-nantes.fr/api/extended/activites/individu/paiement?idIndividu={self.username}&typeIndividu={self.getEtudiant()["type"]}&idPeriode={self.id_periode}'
        rep = self.session.get(url_3sports).json()
        
        activities = []
        for activity in rep['activites'] :
            activities.append(activity['id'])
            
        return activities
    
    def getActivitiesInfo(self):
        '''
        Renvoie un dataframe avec toutes les infos sur les créneaux disponibles
        '''
        activities_list = []
        ordered_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        for activity_id in self.getActivities():
            URL = f'https://u-sport.univ-nantes.fr/api/extended/creneau-recurrents/semaine?idActivite={activity_id}&idPeriode={self.id_periode}&idIndividu={self.username}'
            rep = self.session.get(URL).json()

            if len(rep) > 0 : 
                activity_name = rep[0]["activite"]['nom']
                for activity in rep:
                    jour = activity['jour'].capitalize()
                    creneau_horaire = activity['horaireDebut'] + ' - ' + activity['horaireFin']
                    lieu = activity['localisation']['nom']
                    
                    activities_list.append({
                        'activity_name': activity_name,
                        'activity_id': activity_id,
                        'jour': jour,
                        'creneau_horaire': creneau_horaire,
                        'lieu' : lieu,
                        'places_restantes' : activity['quota'] - activity['nbInscrits'],
                        'id': activity['id']
                    })
            
        df = pd.DataFrame(activities_list)
        df['jour'] = pd.Categorical(df['jour'], categories=ordered_days, ordered=True)
        df = df.sort_values(['jour', 'creneau_horaire'])
        df.reset_index(inplace=True, drop=True) 
            
        return df
        
    def printIDs(self) :
        print(self.getActivitiesInfo().drop(["activity_id"], axis = 1))
    
    def reserverCreneau(self, liste_input : list[str] = []) :
        '''
        Affiche la data frame et prend un input utilisateur pour réserver un créneau
        Si aucun argument n'est spécifié, on print le tableau et on demande à l'utilisateur de saisir les créneaux qu'il veut.
        Sinon, on réserve les créneaux de *args.
        '''
        df = self.getActivitiesInfo()
        
        if liste_input == [] :
            print(df.drop(['activity_id', 'id'], axis=1))
        
            input_user = input('Entrez le numéro des créneaux que vous voulez réserver, avec des espaces.\nPar exemple, 10 2 réserve les créeaux 10 et 2\n$> ')
            liste_indexes = input_user.split(' ')
            
            if None in liste_indexes :
                liste_indexes.pop(None)
            
            if '' in liste_indexes :
                liste_indexes.pop('')
                
            try :
                liste_indexes = list(map(lambda x : int(x), liste_indexes))
        
            except ValueError :
                print('Entrée non valide')
                return
        
        else :
            liste_indexes = []
            for id_creneau in liste_input : 
                for i in range(df.shape[0]) : 
                    if id_creneau == df.iloc[i]['id'] :
                        liste_indexes.append(i)   
         
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))                   
        for index_input in liste_indexes :
            print('\t - ', end='')
            try :
                activity_id = df.iloc[index_input]['activity_id']
                creneau_id = df.iloc[index_input]['id']
                places_restantes = df.iloc[index_input]['places_restantes']
            except :
                print('Valeur d\'index non valide')
                return
            else :
                if places_restantes > 0 :
                    if self.poster_requete(creneau_id, activity_id) :
                        print(f"Inscription effectuée en {df.iloc[index_input]['activity_name']}, le {df.iloc[index_input]['jour']} pour le créneau de {df.iloc[index_input]['creneau_horaire']}")

                    else :
                        print(f"Erreur d'inscription en {df.iloc[index_input]['activity_name']}, le {df.iloc[index_input]['jour']} pour le créneau de {df.iloc[index_input]['creneau_horaire']}")
                
                else :
                    print(f"Pas de place en {df.iloc[index_input]['activity_name']}, le {df.iloc[index_input]['jour']} pour le créneau de {df.iloc[index_input]['creneau_horaire']}")
        print()


    def poster_requete(self, id_creneau, id_activite):
        '''
        Envoie une requête POST pour réserver un créneau
        '''
        postURL = f'https://u-sport.univ-nantes.fr/api/extended/reservation-creneaux?idPeriode={self.id_periode}'

        post_data = {
            "utilisateur": {
                "login": self.username,
                "typeUtilisateur": self.getEtudiant()["type"]
            },
            'dateReservation': datetime.datetime.now().isoformat(timespec='milliseconds') + 'Z',
            'actif': False,
            'forcage': False,
            'creneau': self.getCreneau(id_creneau,id_activite),
            "individuDTO": self.getEtudiant()
        }
        
        post_data["creneau"]["fileAttente"] = True
        post_data["creneau"]["actif"] = True
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Convertir les données en JSON
        post_data_json = json.dumps(post_data)

        rep = self.session.post(postURL, 
                                data = post_data_json, 
                                headers = headers)

        return rep.status_code == 201
    
    def logout(self) : 
        self.session.close()

def readJSON() :
    with open('config.json', 'r') as file :
        return dict(json.load(file))

def setSchedule(day, hour, actions) :
    match day :
        case "lundi" :
            schedule.every().monday.at(hour).do(actions)
        case "mardi" :
            schedule.every().tuesday.at(hour).do(actions)
        case "mercredi" :
            schedule.every().wednesday.at(hour).do(actions)
        case "jeudi" :
            schedule.every().thursday.at(hour).do(actions)
        case "vendredi" :
            schedule.every().friday.at(hour).do(actions)
        case "samedi" :
            schedule.every().saturday.at(hour).do(actions)
        case "dimanche" :
            schedule.every().sunday.at(hour).do(actions)

def setAllSchedules(actions) :
    dico = readJSON()
    for day in dico["jours"] :
        for hour in dico["jours"][day] :
            setSchedule(day, hour, actions)