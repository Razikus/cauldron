from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CauldronHost import *
from Base import Base
from flask import Flask

app = Flask(__name__)

def createEngine():
    print "LEOLELELAELLE"
    return create_engine('sqlite:///:memory:', echo=True)

def createSessionMaker(engine):
    return sessionmaker(bind=engine)

engine = createEngine()
SessionMaker = createSessionMaker(engine)

@app.route("/")
def all():
    session = SessionMaker()
    result = session.query(CauldronHost).all()
    session.commit()


    return str(result)

@app.route("/createSchema")
def createSchema():
    createDBSchema(engine)
    return constructOKStatus()


@app.route("/addHost/<host>", defaults = {'group' : None})
@app.route("/addHost/<host>/<group>")
def addHost(host, group):
    session = SessionMaker()
    addHostToBase(session, host = host, group = group)
    session.commit()
    return constructOKStatus()


def createDBSchema(engine):
    Base.metadata.create_all(engine);


def getSession(sessionMaker):
    return sessionMaker();

def addHostToBase(session, host, group = None):
    host = CauldronHost(ip = host)
    session.add(host)

def constructOKStatus():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7777)
