from flask import Flask
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
from flask_mongoengine import MongoEngine

app.config["MONGODB_SETTINGS"] = {"DB": "heroku_nb42cvd6",
                                  "HOST": "mongodb://heroku_nb42cvd6:nhl0pikbf3301kd6qjnagc7s6o@ds147069.mlab.com:47069/heroku_nb42cvd6"}
app.config["SECRET_KEY"] = "Sekretiki_Hala"


db = MongoEngine(app)


def register_blueprints(app):
    # Prevents circular imports
    from views.views import posts
    from views.views import about
    from views.views import contact
    from views.views import portfolio
    from views.views import hello
    from admin.admin import admin
    app.register_blueprint(hello)
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(about)
    app.register_blueprint(portfolio)
    app.register_blueprint(contact)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
