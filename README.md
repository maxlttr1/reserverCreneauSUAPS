## Bonjour !
Le SUAPS (service sports de Nantes Université) propose des créneaux horaires pour faire du sport, cependant ces créneaux sont très vite remplis.
J'ai donc fait un petit programme qui permet de réserver des créneaux sans s'embêter à se connecter à son compte, etc.

Tout se fait avec des requêtes GET/POST. J'ai utilisé [Burp Suite](https://portswigger.net/burp/releases/professional-community-2024-8-5?requestededition=community&requestedplatform=). C'est un outil qui permet d'intercepter les requêtes, voir leur contenu, etc. Cela m'a permis de savoir à quels URLs GET, et quel contenu. Cela m'a aussi aidé pour savoir quelle data JSON il fallait POST pour résever un créneau, ce qui m'a permis de reconstruire le JSON et de réussir la requête POST.

Tout ce dont vous aurez besoin, c'est de votre username et password, et je suppose qu'il faut que vous ayez adhéré au SUAPS.


### Fonctionnement
On fait tourner le programme une première fois pour récupérer les IDs des créneaux qu'on veut réserver de manière automatique. Ensuite, on les place dans config.json et on laisse le programme faire !

### Ce que vous devez faire
- Cloner le dépot :
    ```bash
    git clone https://github.com/flash2974/reserverCreneauSUAPS && cd reserverCreneauSUAPS/
    ```
- Dans `config/` renommer `.example.env` en `.env`, et `example.config.json` en `config.json` : 
    ```bash
    mv config/.example.env config/.env && mv config/example.config.json config/config.json
    ```

- Ouvrir le fichier `.env` et remplir les champs **USERNAME** et **PASSWORD**
    ```bash
    echo -e "USERNAME=username\nPASSWORD=mdp\n" > config/.env
    ```

#### Avec Docker:
```bash
docker compose up -d
```
- Ensuite, vous aurez accès à la *WebUI*. Dans un navigateur, allez à l'adresse de votre serveur (IP ou nom de domaine) et mettez vous sur le port 5000. Il faut au préalabale que le port soit ouvert.

    - Si vous faites tourner en local : [**http://localhost:5000**](http://localhost:5000)
    - Si vous hébergez sur un serveur : **http://IP_de_mon_serveur:5000**

Connectez-vous sur la WebUI à l'aide de votre mot de passe universitaire (celui enregistré dans le .env)
Il vous suffira de cocher les **activités** qui vous intéressent et de sauvegarder. Les horaires d'activation du bot sont automatiquement définies.

<br>

- Pour mettre à jour le container:

    ```bash
    docker compose down && \
    docker rmi reservercreneausuaps-app && \
    git pull && \
    docker compose up -d --build
    ```
    
<br>

Configuration HTTPS Avec Caddy
1. Installer Caddy :
```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo tee /etc/apt/trusted.gpg.d/caddy.asc
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy.list
sudo apt update
sudo apt install caddy
```

2. Création du fichier de configuration (Caddyfile) : Remplacer `mon-domaine.fr` par nom de domaine
```
mon-domaine.fr { 
    reverse_proxy localhost:5000
}
```

3. Démarrer Caddy
```bash
sudo systemctl restart caddy
```

De cette manière, on accède au site directement via `https://mon-domaine.fr`.
Ensuite, on peut accéder à la page principale sans passer par la login page.
Pour ce faire :

1. Ajout du token au fichier `.env`
```bash
openssl rand -hex 32 >> config/.env
```

2. Copiez ce token !
```bash
cat config/.env
```

3. Relancez le container docker :
```bash
docker compose down && \
docker rmi reservercreneausuaps_app && \
docker compose up -d --build
```

4. Accédez directement au site via l'url suivante :
```
https://{nom_de_domaine}/login?token={token}
```

Merci à [maxlttr](https://github.com/maxlttr1) pour son aide !