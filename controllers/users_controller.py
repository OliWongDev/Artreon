from flask import Blueprint, request, abort
from main import db
from models.users import User, UserSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize_precise_user
users = Blueprint("users", __name__, url_prefix="/users")



# 127.0.0.1:5000/users
# This returns the users
# WORKING 14/11/22
@users.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
     users_list = db.select(User).order_by(User.id.asc())
     result = db.session.scalars(users_list)
     if result:
          return UserSchema(many=True, exclude=['password']).dump(result), 200
     else:
        return {"error": "No users found on the database"}, 404

#127.0.0.1:5000/users/<int:id>
# This returns a single user
# WORKING 14/11/22
@users.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_user(id):
    user = db.select(User).filter_by(id=id)
    result = db.session.scalar(user)
    if result:
          return UserSchema(exclude=['password']).dump(result), 200
    else:
        return {"error": "No users found on the database"}, 404

# 127.0.0.1/5000/users/<string:user_alias>
# This acquires the user by their alias
# WORKING 14/11/22
@users.route("/<string:user_alias>", methods=["GET"])
@jwt_required()
def get_user_by_alias(user_alias):
    artist = db.select(User).filter_by(user_alias=user_alias)
    result = db.session.scalar(artist)
    if result:
          return UserSchema(exclude=['password']).dump(result), 200
    else:
        return {"error": "No users found on the database"}, 404

# 127.0.0.1:5000/users/<string:user_alias>
# This allows a user to update their details
# WORKING 14/11/22
@users.route("/<string:user_alias>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user_details(user_alias):
    user_data = db.select(User).filter_by(user_alias=user_alias)
    user = db.session.scalar(user_data)
    user_id = user.id
    authorize_precise_user(user_id)
    if user:
        user.user_alias = request.json.get("user_alias") or user.user_alias
        user.first_name = request.json.get("first_name") or user.first_name
        user.last_name = request.json.get("last_name") or user.last_name
        user.email = request.json.get("email") or user.email
        user.has_subscription = request.json.get("has_subscription") or user.has_subscription
        user.password = request.json.get("password") or user.password
        return UserSchema(exclude=['password']).dump(user), 200
    else:
        return abort(404, description="The user does not exist")

# 127.0.0.1:5000/users/<string:user_alias>
# Delete a user
# WORKING 14/11/22
@users.route("/<string:user_alias>", methods=["DELETE"])
@jwt_required()
def delete_user_account(user_alias):
    user_statement = db.select(User).filter_by(user_alias=user_alias)
    user = db.session.scalar(user_statement)
    user_id = user.id
    authorize_precise_user(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f"The user '{user_alias}' was deleted successfully"}, 200
    else:
        return {"error": f"The user with the name {user_alias} was not found to be deleted."}, 404


# 127.0.0.1:5000/users/<string:user_alias>/comments
# View all comments a user has made.
# WORKING 14/11/22
@users.route("/<string:user_alias>/comments", methods=["GET"])
@jwt_required()
def get_all_user_comments(user_alias):
    user_statement = db.select(User).filter_by(user_alias=user_alias)
    user = db.session.scalar(user_statement)
    if user:
        return UserSchema(only=("user_alias", "artwork_comments", "q_and_a_comments", "walkthrough_comments")).dump(user), 200
    else:
        return {"error": f"The user with the user alias '{user_alias}' was not found"}, 404