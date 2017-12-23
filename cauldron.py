import cli.app

@cli.app.CommandLineApp
def cauldron(app):
    print app.params.list
    pass

cauldron.add_param("-l", "--list", help="lists for all avalaible hosts and groups", default = False, action = "store_true")

if __name__ == "__main__":
    cauldron.run()
