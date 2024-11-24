### Bonjour !
Le SUAPS (service sports de Nantes Université) propose des créneaux horaires pour faire du sport, cependant ces créneaux sont très vite remplis.
J'ai donc fait un petit programme qui permet de réserver des créneaux sans s'embêter à se connecter à son compte, etc.

Tout se fait avec des requêtes GET/POST. J'ai utilisé [Burp Suite](https://portswigger.net/burp/releases/professional-community-2024-8-5?requestededition=community&requestedplatform=). C'est un outil qui permet d'intercepter les requêtes, voir leur contenu, etc. Cela m'a permis de savoir à quels URLs GET, et quel contenu. Cela m'a aussi aidé pour savoir quelle data JSON il fallait POST pour résever un créneau, ce qui m'a permis de reconstruire le JSON et de réussir la requête POST.

Tout ce dont vous aurez besoin, c'est de votre username et password, et je suppose qu'il faut que vous ayez adhéré au SUAPS.

Deux manières de fonctionner :
- "Basique" : le programme renvoie un tableau avec tous les IDs des activités, vous choisissez celles que vous voulez
- Ou vous rentrez des IDs dans une liste python et c'est très facilement automatisable. Dans ce cas, utilisez le module `schedule`, pour régler le jour et l'heure de vos réservations.

Ce que vous devez faire : 
- Cloner le dépot :
```bash
git clone https://github.com/flash2974/reserverCreneauSUAPS
```
- Renommer `.example.env` en `.env`, l'ouvrir et remplir les champs **USERNAME** et **PASSWORD** 

<br>

Si vous utilisez Docker :
```bash
docker-compose up -d
```

<br>

Sinon :
1. Installez tous les modules nécessaires avec :
    ```bash
    pip install -r requirements.txt
    ```

    Si pip n'est pas trouvé, essayez : 
    ```bash
    python.exe -m pip install -r requirements.txt
    ```

2. Lancez `main.py` : 
   - Soit dans un IDE
   - Soit dans un terminal avec : 
        ```bash
        python main.py
        ```
