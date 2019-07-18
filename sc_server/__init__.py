from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/base.db'
db = SQLAlchemy(app)

# import ovde jer sc_server.models koristi promenljivu db
from sc_server.models import *

# pravljenje nove baze ukoliko je prethodna obrisana (promene u modelima
# zahtevaju brisanje baze i pravljenje nove)
if not os.path.isfile('data/base.db'):
    db.create_all()

from sc_server import routes