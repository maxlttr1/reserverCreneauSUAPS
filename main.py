from Fonctions import AutoSUAPS

LOGIN_URL = 'https://cas6.univ-nantes.fr/esup-cas-server/login?service=https%3A%2F%2Fu-sport.univ-nantes.fr%2Fcas%2F'
username = ...
password = ...

auto = AutoSUAPS(username, password, LOGIN_URL)

auto.reserverCreneau() # Commencer par ça
# auto.reserverCreneau(14, 18, 21) # Réserve les créneaux
