from flask import Flask
import config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
#app.config.from_object('config')
#Bootstrap(app)
from app import views


def main():
    app.config.from_object('config')
    Bootstrap(app)

if __name__ == "__main__":
    main()
    print "meh"
    app.run()
