from app import db

class Meal(db.Model):
    #meal_id
    meal_id = db.Column(db.Integer(), primary_key=True)
    #name
    name = db.Column(db.String(80), nullable=False)
    #desc
    description = db.Column(db.String(80), nullable=False)
    #weight
    weight = db.Column(db.Float(), nullable=False)
    #calories
    calories = db.Column(db.Integer(), nullable=False)
    #price
    price = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return "Name: {}, Description: {}, Weight: {:.2f}, Calories: {:d}, Price: {:.2f}".format(self.name, self.description, self.weight, self.calories, self.price)
