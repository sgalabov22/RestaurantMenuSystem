import os
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mealdatabase.db"))

app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import models
from .models import Meal

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

def create_app():
    @app.route("/", methods=["GET"])
    @app.route("/index", methods=["GET"])
    def home():
        return render_template("home.html")

    @app.route("/create", methods=["GET", "POST"])
    def create():
        return render_template("create.html")

    @app.route("/update", methods=["GET", "POST"])
    def update():
        oldmeal_id = request.args.get("oldmeal_id")
        oldmeal = Meal.query.filter_by(meal_id=oldmeal_id).first()
        return render_template("update.html", oldmeal=oldmeal)

    return app
