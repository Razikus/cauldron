from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CauldronHost import *
from CauldronGroup import *
from CauldronGroupHostAssoc import *
from Base import Base
from flask import Flask
from flask import jsonify
from flask_marshmallow import Marshmallow
from Base import ma
from Base import app


def createEngine():
    return create_engine('sqlite:///:memory:', echo=True)

def createSessionMaker(engine):
    return sessionmaker(bind=engine)

engine = createEngine()
SessionMaker = createSessionMaker(engine)

@app.route("/createSchema")
def createSchema():
    createDBSchema(engine)
    return constructOKStatus()


@app.route("/host/<host>", defaults = {'group' : None}, methods=["GET"])
@app.route("/host/<host>/<group>", methods=["GET"])
def addHost(host, group):
    session = SessionMaker()
    addHostToBase(session, hostName = host, groupName = group)
    session.commit()
    return constructOKStatus()

@app.route("/host", methods=["GET"])
def getHosts():
    session = SessionMaker()
    result = session.query(CauldronHost).all()
    session.commit()
    cauldronHostsSchema = CauldronHostSchema(many = True)
    dump = cauldronHostsSchema.dump(result)
    return jsonify(dump.data)

def createDBSchema(engine):
    Base.metadata.create_all(engine);

def getSession(sessionMaker):
    return sessionMaker();

def addHostToBase(session, hostName, groupName = None):
    host = CauldronHost(ip = hostName)
    if groupName is not None:
        group = CauldronGroup(name = groupName)
        assoc = CauldronGroupHostAssoc()
        assoc.group = group
        host.groups.append(assoc)
    session.add(host)

def constructOKStatus():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7777)
