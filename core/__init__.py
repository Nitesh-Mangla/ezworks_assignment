from core.application import Application

application = Application()
app = application.app


# check if environment is not set to development then give a message to developer or tester to set env
if app.config['ENV'] != 'development':
    print("Please set your environment to development and to set use `export FLASK_ENV=development`")
    exit()
else:
    # load configuration for development
    app.config.from_object('config.config.Development')

