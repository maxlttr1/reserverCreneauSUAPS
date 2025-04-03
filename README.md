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
- Dans `config/` renommer `.example.env` en `.env`, et `example.config.json` en `config.json` (1) : 
    ```bash
    mv config/.example.env config/.env && mv config/example.config.json config/config.json
    ```

- Ouvrir le fichier `.env` et remplir les champs **USERNAME** et **PASSWORD**
    ```bash
    echo -e "USERNAME=username\nPASSWORD=mdp" > config/.env
    ```

#### Avec Docker :
```bash
docker compose up -d
```
- Visiter [**http://localhost:5000**](http://localhost:5000): il vous suffira de cocher les **activités** qui vous intéressent et de sauvegarder. Les horaires d'activation du bot sont automatiquement définies.
- Pour mettre à jour le container:

    ```bash
    docker compose down && \
    docker rmi reservercreneausuaps-app && \
    git pull && \
    docker compose up -d --build
    ```

<br>

### TODO :
- fix `setIdPeriode()` dans `Fonctions.py` qui fixe le mauvais ID de période une semaine avant la période "spéciale" (Noël)
- limiter le nombre d'activités sélectionnables dans la web_ui

<br>
<br>

(1) Si vous voulez faire des pulls requests, copiez et renommez.
```bash
cp config/.example.env config/.env && cp config/example.config.json config/config.json
```

<br>

Merci à [maxlttr](https://github.com/maxlttr1) pour son aide !
