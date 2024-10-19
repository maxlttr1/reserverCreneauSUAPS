### Bonjour !
Le SUAPS (service sports de Nantes Université) propose des créneaux horaires pour faire du sport, cependant ces créneaux sont très vite remplis.
J'ai donc fait un petit programme qui permet de réserver des créneaux sans s'embêter à se connecter à son compte, etc.

Tout se fait avec des requêtes GET/POST. J'ai utilisé [Burp Suite](https://portswigger.net/burp/releases/professional-community-2024-8-5?requestededition=community&requestedplatform=) pour savoir à quels URLs GET, et quel contenu. Cela m'a aussi aidé pour savoir quelle data JSON il fallait POST pour résever un créneau, ce qui m'a permis de reconstruire le JSON et de réussir la requête POST.

Tout ce dont vous aurez besoin, c'est de votre username et password, et je suppose qu'il faut que vous ayez adhéré au SUAPS.

Avec ce bout de code, il sera très simple d'automatiser complètement la réservation de créneau et de ne plus avoir de problème de place.
En effet, pour le moment on a besoin d'un input utilisateur, cependant vous pouvez récupérer directement l'ID du créneau et de l'activité pour réserver automatiquement, sans prendre l'input user.

Ce que vous devez faire : 
1. Renommez `.example.env` en `.env`, l'ouvrir et remplir les champs **USERNAME** et **PASSWORD**

2. Installez tous les modules nécessaires avec :
    ```bash
    pip install -r requirements.txt
    ```

    Si pip n'est pas trouvé, essayez : 
    ```bash
    python.exe -m pip install -r requirements.txt
    ```

3. Lancez `main.py` : 
   - Soit dans un IDE
   - Soit dans un terminal avec : 
        ```bash
        python main.py
        ```
