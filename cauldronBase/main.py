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

@app.route("/host/<host>/<group>", methods=["DELETE"])
@app.route("/host/<host>", defaults = {'group' : None}, methods=["DELETE"])
def removeHost(host, group):
    session = SessionMaker()
    removeHostFromBase(session, hostName = host, groupName = group)
    session.commit()
    return constructOKStatus()

def removeHostFromBase(session, hostName, groupName = None):
    return "Not yet implemented"

@app.route("/host/<host>/<group>", methods=["POST"])
@app.route("/host/<host>", defaults = {'group' : None}, methods=["POST"])
def addHost(host, group):
    session = SessionMaker()
    addHostToBase(session, hostName = host, groupName = group)
    session.commit()
    return constructOKStatus()


@app.route("/group/<group>", methods = ["POST"])
def addGroup(group):
    session = SessionMaker()
    addHostToBase(session, groupName = group);
    session.commit()
    return constructOKStatus()

@app.route("/host", defaults = {'group' : None}, methods=["GET"])
@app.route("/host/<group>", methods=["GET"])
def getHosts(group):
    session = SessionMaker()
    if group is not None:
        result = session.query(CauldronHost).all()
    else:
        result = session.query(CauldronHost).all()
    session.commit()
    cauldronHostsSchema = CauldronHostSchema(many = True)
    dump = cauldronHostsSchema.dump(result)
    return jsonify(dump.data)

def createDBSchema(engine):
    Base.metadata.create_all(engine);

def getSession(sessionMaker):
    return sessionMaker();

def addHostToBase(session, hostName = None, groupName = None):
    if hostName is None and groupName is not None:
        group = CauldronGroup(name = groupName)
        session.add(group)
    elif hostName is not None and groupName is None:
        host = CauldronHost(ip = hostName)
        session.add(host)
    elif hostName is not None and groupName is not None:
        group = session.query(CauldronGroup).filter_by(name = groupName).first()
        if(group is None):
            addHostToBase(session, groupName = groupName)
            return addHostToBase(session, hostName, groupName)
        host = session.query(CauldronHost).filter_by(ip = hostName).first()
        if(host is None):
            addHostToBase(session, hostName = hostName)
            return addHostToBase(session, hostName, groupName)

        assoc = CauldronGroupHostAssoc()
        assoc.group = group
        assoc.host = host
        host.groups.append(assoc)
        session.add(host)

def constructOKStatus():
    return '{ "status" : "OK"}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=7777)
