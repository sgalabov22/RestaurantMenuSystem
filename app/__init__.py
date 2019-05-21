import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mealdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import models
from .models import Meal

def create_app():
    @app.route("/", methods=["GET"])
    def home():
        meals = Meal.query.all()
        return render_template("home.html", meals=meals)

    @app.route("/create", methods=["GET", "POST"])
    def create():
        if request.form:
            new_meal = Meal(name=request.form.get("name"),
                            description=request.form.get("description"),
                            weight=request.form.get("weight"),
                            calories=request.form.get("calories"),
                            price=request.form.get("price"))
            db.session.add(new_meal)
            db.session.commit()
            return redirect("/")

        return render_template("create.html")

    return app
