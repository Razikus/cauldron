import cli.app
import requests
from pprint import pprint

configHost = "http://localhost"
configPort = "7777"
configURL = configHost + ":" + configPort


@cli.app.CommandLineApp
def cauldron(app):

    addFlag = app.params.add
    listFlag = app.params.list
    deleteFlag = app.params.delete

    host = app.params.host
    group = app.params.group

    if(checkForExclusive(addFlag, listFlag, deleteFlag)):
        print "Provide one of the -a -l or -d"
        exit(1)

    if(host is None and group is None and not listFlag):
        print "Host and group are none, see -h to get help"
        exit(1)

    if addFlag:
        pprint(addToBase(host, group))
    elif listFlag:
        pprint(listFromBase(host, group))
    elif deleteFlag:
        pprint(deleteFromBase(host, group))
    pass

def deleteFromBase(host, group):
    if(group is not None and host is None):
        return removeGroupFromBase(group)
    elif(host is not None and group is None):
        return removeHostFromBase(host);
    else:
        return removeHostFromGroup(host, group)

def listFromBase(host, group):
    if(group is not None and host is None):
        return listGroupFromBase(group)
    elif(host is not None and group is None):
        return listHostFromBase(host);
    elif(host is None and group is None):
        return listHosts();
    else:
        return listHostFromGroup(host, group)

def addToBase(host, group):
    if(group is not None and host is None):
        return addGroupToBase(group)
    elif(host is not None and group is None):
        return addHostToBase(host);
    else:
        return addHostToGroup(host, group)

def listGroupFromBase(group):
    return group
def listHostFromBase(host):
    return host
def listHostFromGroup(host, group):
    return host + " " + group
def listHosts():
    return jsonREQ(met = "GET", path = "host")

def removeGroupFromBase(group):
    return group
def removeHostFromBase(host):
    return host
def removeHostFromGroup(host, group):
    return host + " " + group

def addGroupToBase(group):
    return "Not implemented"
def addHostToBase(host):
    return jsonREQ(met = "POST", path = "host/" + host)
def addHostToGroup(host, group):
    return jsonREQ(met = "POST", path = "host/" + host + "/" + group)

def checkForExclusive(addFlag, listFlag, deleteFlag):
    summed = sum([addFlag, listFlag, deleteFlag])
    if(summed > 1 or summed == 0):
        return True
    else:
        return False

def jsonREQ(**kwargs):
    met = kwargs["met"]
    if met is None:
        return ""
    else:
        if met == "GET":
            return jsonGET(**kwargs)
        elif met == "POST":
            return jsonPOST(**kwargs)
        elif met == "DELETE":
            return jsonDELETE(**kwargs)

def jsonPOST(**kwargs):
    relativePath = kwargs["path"]
    url = configURL + "/" + relativePath
    return requests.post(url).json()
def jsonDELETE(**kwargs):
    relativePath = kwargs["path"]
    url = configURL + "/" + relativePath
    return requests.delete(url).json()
def jsonGET(**kwargs):
    relativePath = kwargs["path"]
    url = configURL + "/" + relativePath
    return requests.get(url).json()

cauldron.add_param("-host", "--host", help="provide host to the command", default = None)
cauldron.add_param("-group", "--group", help="provide a group to the command", default = None)
cauldron.add_param("-a", "--add", help="add host to the base", default = False, action = "store_true")
cauldron.add_param("-l", "--list", help="lists for all avalaible hosts and groups", default = False, action = "store_true")
cauldron.add_param("-d", "--delete", help="delete option", default = False, action = "store_true")

if __name__ == "__main__":
    cauldron.run()
