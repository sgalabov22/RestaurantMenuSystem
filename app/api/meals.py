from flask import jsonify, request, url_for
from app import db
from app.models import Meal
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import auth

@bp.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
    return jsonify(Meal.query.get_or_404(id).to_dict())

@bp.route('/meals', methods=['GET'])
def get_meals():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 5, type=int)
    data = Meal.to_collection_dict(Meal.query, page, per_page, 'api.get_meals')

    if data == -1:
        response = jsonify({'error': 'Not found'})
        response.status_code = 404
        return response

    return jsonify(data)

@bp.route('/meals', methods=['POST'])
@auth.login_required
def create_meal():
    data = request.get_json() or {}

    meal = Meal()
    if (meal.from_dict(data) == -1):
        return bad_request('must include all fields')
    else:
        db.session.add(meal)
        db.session.commit()
        response = jsonify(meal.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_meal', id=meal.meal_id)
        return response

@bp.route('/meals/<int:id>', methods=['PUT'])
@auth.login_required
def update_meal(id):
    meal = Meal.query.get_or_404(id)
    data = request.get_json() or {}

    if meal.from_dict(data) == -1:
        response = jsonify({'error': 'Partial content'})
        response.status_code = 206
        return response
    db.session.commit()
    return jsonify(meal.to_dict())

@bp.route('/meals/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response
