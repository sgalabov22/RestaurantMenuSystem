import os
from flask import Flask, render_template, request, redirect, url_for
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
    @app.route("/index", methods=["GET"])
    def home():
        page = request.args.get("page", 1, type=int)
        meals = Meal.query.order_by(Meal.price.desc()).paginate(page, 2, True)

        if meals.has_next:
            next_url = url_for("home", page=meals.next_num)
        else:
            next_url = None

        if meals.has_prev:
            prev_url = url_for("home", page=meals.prev_num)
        else:
            prev_url = None

        return render_template("home.html", meals=meals.items, next_url=next_url, prev_url=prev_url)

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

    @app.route("/delete", methods=["POST"])
    def delete():
        name_delete = request.form.get("name")
        meal = Meal.query.filter_by(name=name_delete).first()
        db.session.delete(meal)
        db.session.commit()

        return redirect("/")

    @app.route("/update", methods=["GET", "POST"])
    def update():
        oldmeal_id = request.args.get("oldmeal_id")
        oldmeal = Meal.query.filter_by(meal_id=oldmeal_id).first()
        return render_template("update.html", oldmeal=oldmeal)

    @app.route("/update_form", methods=["POST"])
    def update_form():
        oldmeal_id = request.form.get("btn")
        oldmeal = Meal.query.filter_by(meal_id=oldmeal_id).first()

        oldmeal.name = request.form.get("newname")
        oldmeal.description = request.form.get("newdescription")
        oldmeal.weight = request.form.get("newweight")
        oldmeal.calories = request.form.get("newcalories")
        oldmeal.price = request.form.get("newprice")

        db.session.commit()
        return redirect("/")

    return app
