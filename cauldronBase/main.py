from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CauldronHost import *
from Base import Base
from flask import Flask

app = Flask(__name__)

def createEngine():
    return create_engine('sqlite:///:memory:', echo=True)

def createSessionMaker(engine):
    return sessionmaker(bind=engine)

engine = createEngine()
SessionMaker = createSessionMaker(engine)

@app.route("/")
def hello_world():
    createSchema(engine)
    session = SessionMaker()
    addHost("127.0.0.1", session)
    return str(session.query(CauldronHost).first())

def createSchema(engine):
    Base.metadata.create_all(engine);


def getSession(sessionMaker):
    return sessionMaker();

def addHost(ip, session):
    host = CauldronHost(ip=ip)
    session.add(host)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7777)
