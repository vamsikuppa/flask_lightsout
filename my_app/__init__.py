from flask import Flask

app = Flask(__name__)

from my_app.product.views import app

# app.register_blueprint(trigger_blueprint)
