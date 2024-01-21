import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient # ouv sess° aup de mongodb pr se connecter à DB
from dotenv import load_dotenv

load_dotenv()   # peuple var d'envt à partir du ctenu du fi .env qu'on cree et remplit prealablement -> garde secrets en dehors de app.py

def create_app():   # au deploiement le fi se lance parfois en boucle-> cree autent d'app & mongo clt, ms pas ac cette fc° qui wrappe l'appli empêchant cre° pls apps & clt mongo (et mieux pr tester l'appli)
    app = Flask(__name__)       # cree app -> app factory pattern
    client = MongoClient(os.getenv("MONGODB_URI")) # client: conx à MongoDB server
    app.db = client.microblog    # methode .microblog pr conx à DB 'microblog'; wrapping ac app pr stocker DB value inside the app (hors de l'app +tard ds le crs)

    @app.route("/", methods=["GET", "POST"])    # /car requête arrive à la même page d'où elle part (sinon ici par ex "/entry" et ds html->action="/entry")
    def home():
        # print([e for e in app.db.entries.find({})])  # acces à collec° 'entries' de la DB, et trouve tt deds(dict vide en arg dde find)
        if request.method == "POST":
            entry_content = request.form.get("content")    # "content" -> nom de la 'textarea' du formulaire
            formatted_date = datetime.datetime.today().strftime("%d-%m-%y") # datetime object: today date d'aujourd'hui, strftime:format ici 2024-1-15 (%y:24 vs 2024)
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [       # l par comprehension: renvoie 1 l de tuple() à 3 elts
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%d-%m-%y").strftime("%d %b")
            )
            for entry in app.db.entries.find({})        # ds collec entries de la DB  trouve une sorte de l de dict et renvoie val des clefs dem pr chq elt (dict)
        ]
        return render_template("home.html", entries=entries_with_date)

    return app      # run flask interface voit create_app() -> l'exe pr creer l'app -> pr cela la fc° doit retrner var app def à son debut (sinon l'app se lance pas)
