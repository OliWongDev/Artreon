from flask import Blueprint, request
from main import db
from models.walkthroughs import Walkthrough, WalkthroughSchema
from controllers.auth_controller import authorize_artist, authorize_precise_artist, authorize_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

walkthroughs = Blueprint("walkthroughs", __name__, url_prefix="/walkthroughs")

# 127.0.0.1:5000/walkthroughs
# This returns the walkthroughs
# WORKING 14/11/22
@walkthroughs.route("/", methods=["GET"])
@jwt_required()
def get_all_walkthroughs():
    authorize_user()
    walkthroughs_list = db.select(Walkthrough).order_by(Walkthrough.id.asc())
    result = db.session.scalars(walkthroughs_list)
    if result:
          return WalkthroughSchema(many=True).dump(result), 200
    else:
        return {"error": "No walkthroughs found on the database"}, 404

# 127.0.0.1:5000/walkthroughs/<int:id>
# This returns a single walkthrough
# WORKING 14/11/22
@walkthroughs.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_walkthrough(id):
    authorize_user()
    walkthrough = db.select(Walkthrough).filter_by(id=id)
    result = db.session.scalar(walkthrough)
    if result:
        return WalkthroughSchema().dump(result), 200
    else:
        return {"error": f"Walkthrough with id '{id}' not found on the database"}, 404

# 127.0.0.1:5000/walkthroughs
# This adds a walkthrough to the database
# WORKING 14/11/22 
@walkthroughs.route("/", methods=["POST"])
@jwt_required()
def create_artwork():
    authorize_artist()
    walkthrough_fields = WalkthroughSchema().load(request.json)

    new_walkthrough = Walkthrough(
          description = walkthrough_fields["description"],
          date = date.today(),
          artwork_id = walkthrough_fields['artwork_id'],
          artist_id = get_jwt_identity()
    )

    db.session.add(new_walkthrough)
    db.session.commit()

    return WalkthroughSchema().dump(new_walkthrough), 201

# 127.0.0.1:5000/walkthroughs/<int:id>
# This deletes a walkthrough in the database
# WORKING 14/11/22
@walkthroughs.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_walkthrough(id):
    walkthrough_delete_statement = db.select(Walkthrough).filter_by(id=id)
    walkthrough = db.session.scalar(walkthrough_delete_statement)
    artist_id = walkthrough.artist_id
    authorize_precise_artist(artist_id)
    if walkthrough:
        db.session.delete(walkthrough)
        db.session.commit()
        return {'message': f"Walkthrough with an id '{walkthrough.id} was successfully deleted"}, 200
    else:
        return {'error': "Walkthrough with the id requested was not found to be deleted."}, 404

