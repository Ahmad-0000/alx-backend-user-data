#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users_list = [user.to_json() for user in User.all()]
    return jsonify(all_users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    u = User.get(user_id)
    if u is None:
        abort(404)
    return jsonify(u.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def d_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON if the account has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    u = User.get(user_id)
    if u is None:
        abort(404)
    u.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new account
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "missing email"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "missing password"
    if error_msg is None:
        try:
            u = User()
            u.email = rj.get("email")
            u.password = rj.get("password")
            u.first_name = rj.get("first_name")
            u.last_name = rj.get("last_name")
            u.save()
            return jsonify(u.to_json()), 201
        except Exception as e:
            error_msg = "Can't create account - {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_account(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the account
    """
    if user_id is None:
        abort(404)
    u = User.get(user_id)
    if u is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        u.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        u.last_name = rj.get('last_name')
    u.save()
    return jsonify(u.to_json()), 200
