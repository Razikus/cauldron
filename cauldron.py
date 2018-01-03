import cli.app
import requests

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
        addToBase(host, group)
    elif listFlag:
        listFromBase(host, group)
    elif deleteFlag:
        deleteFromBase(host, group)
    pass

def deleteFromBase(host, group):
    if(group is not None and host is None):
        removeGroupFromBase(group)
    elif(host is not None and group is None):
        removeHostFromBase(host);
    else:
        removeHostFromGroup(host, group)

def listFromBase(host, group):
    if(group is not None and host is None):
        listGroupFromBase(group)
    elif(host is not None and group is None):
        listHostFromBase(host);
    elif(host is None and group is None):
        listHosts();
    else:
        listHostFromGroup(host, group)

def addToBase(host, group):
    if(group is not None and host is None):
        addGroupToBase(group)
    elif(host is not None and group is None):
        addHostToBase(host);
    else:
        addHostToGroup(host, group)

def listGroupFromBase(group):
    print group
def listHostFromBase(host):
    print host
def listHostFromGroup(host, group):
    print host + " " + group
def listHosts():
    print jsonGET()

def removeGroupFromBase(group):
    print group
def removeHostFromBase(host):
    print host
def removeHostFromGroup(host, group):
    print host + " " + group

def addGroupToBase(group):
    print "Adding group " + group + " to base"
def addHostToBase(host):
    print "Adding host " + host + " to base"
def addHostToGroup(host, group):
    print "Adding host " + host + " to group " + group

def checkForExclusive(addFlag, listFlag, deleteFlag):
    summed = sum([addFlag, listFlag, deleteFlag])
    if(summed > 1 or summed == 0):
        return True
    else:
        return False

def jsonGET(*args):
    url = configURL + "/host"
    return str(requests.get(url).json)

cauldron.add_param("-host", "--host", help="provide host to the command", default = None)
cauldron.add_param("-group", "--group", help="provide a group to the command", default = None)
cauldron.add_param("-a", "--add", help="add host to the base", default = False, action = "store_true")
cauldron.add_param("-l", "--list", help="lists for all avalaible hosts and groups", default = False, action = "store_true")
cauldron.add_param("-d", "--delete", help="delete option", default = False, action = "store_true")

if __name__ == "__main__":
    cauldron.run()
