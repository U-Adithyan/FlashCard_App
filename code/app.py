import os
from flask import Flask
from flask_restful import Resource,Api
from application import config
from application.config import DevelopConfig
from application.database import db

app=None
api=None

def create_app():
    app=Flask(__name__,template_folder="templates")
    print("Starting Development")
    app.config.from_object(DevelopConfig)
    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app,api

app,api=create_app()

from application.controllers import *

from application.api import *
api.add_resource(UserAPI,"/user","/user/<string:username>")
api.add_resource(DeckAPI,"/deck/<int:deck_id>")
api.add_resource(CardAPI,"/card/<int:card_id>")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)