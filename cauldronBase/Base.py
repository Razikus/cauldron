from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask import jsonify
from flask_marshmallow import Marshmallow
Base = declarative_base()
app = Flask(__name__)
ma = Marshmallow(app)


