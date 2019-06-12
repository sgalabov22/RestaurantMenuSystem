from app import db
from flask import url_for

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }

        return data

class Meal(PaginatedAPIMixin, db.Model):
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

    def to_dict(self):
        data = {
            'id': self.meal_id,
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
            'calories': self.calories,
            'price': self.price,
            '_links': {
                'self': url_for('api.get_meal', id=self.meal_id)
            }
        }

        return data

    def from_dict(self, data):
        for field in ['name', 'description', 'weight', 'calories', 'price']:
            if field in data:
                setattr(self, field, data[field])
