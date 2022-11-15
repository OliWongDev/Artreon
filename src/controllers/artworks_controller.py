from flask import Blueprint, request
from main import db
from datetime import date
from models.artworks import Artwork, ArtworkSchema
from models.artists import Artist
from models.artwork_comments import ArtworkComment, ArtworkCommentSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize_precise_artist, authorize_artist, authorize_user, authorize_precise_user

artworks = Blueprint('artworks', __name__, url_prefix="/artworks")


# 127.0.0.1:5000/artworks
# This returns the artworks
# WORKING 14/11/22

@artworks.route("/", methods = ["GET"])
@jwt_required()
def get_all_artworks():
     artworks_list = db.select(Artwork).order_by(Artwork.id.asc())
     result = db.session.scalars(artworks_list)
     if result:
          return ArtworkSchema(many=True).dump(result), 200
     else:
        return {"error": "No artworks found on the database"}, 404

# 127.0.0.1:5000/artworks/<int:id>
# This returns a single artwork
# WORKING 14/11/22
@artworks.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_artwork(id):
    artwork = db.select(Artwork).filter_by(id=id)
    artwork_result = db.session.scalar(artwork)
    if artwork_result:
          return ArtworkSchema().dump(artwork_result), 200
    else:
          return {"error": f"The artwork with id {id} was not found"}, 404

#127.0.0.1:5000/artworks
#### This allows the artist to CREATE and post an artwork
# WORKING 14/11/22
@artworks.route("/", methods=["POST"])
@jwt_required()
def create_artwork():
     authorize_artist()
     artwork_fields = ArtworkSchema().load(request.json)

     new_artwork = Artwork(
          artwork_name = artwork_fields["artwork_name"],
          description = artwork_fields["description"],
          date = date.today(),
          artist_id = get_jwt_identity()
     )

     db.session.add(new_artwork)
     db.session.commit()

     return ArtworkSchema().dump(new_artwork), 201


# 127.0.0.1:5000/artworks/<int:id>
# This allows the artist to DELETE an artwork
# WORKING 14/11/22
@artworks.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_artwork(id):
     artwork_delete_statement = db.select(Artwork).filter_by(id=id)
     artwork = db.session.scalar(artwork_delete_statement)
     artist_id = artwork.artist_id
     authorize_precise_artist(artist_id)
     if artwork:
          db.session.delete(artwork)
          db.session.commit()
          return {'message': f"Artwork '{artwork.artwork_name}' deleted successfully"}
     else: 
          return {"error": f"Artwork with id '{id}' was not found to be deleted"}, 404


# 127.0.0.1:5000/artworks/<int:id>
# This allows the artist to update their artwork description
# WORKING 14/11/22
@artworks.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def patch_artwork(id):
     artwork_statement = db.select(Artwork).filter_by(id=id)
     artwork = db.session.scalar(artwork_statement)
     artist_id = artwork.artist_id
     authorize_precise_artist(artist_id)
     if artwork:
          artwork.description = request.json.get('description') or artwork.description
          db.session.commit()
          return ArtworkSchema().dump(artwork)
     else:
          return {'error': f"Artwork not found with id {id} to update description."}, 404
 
# 127.0.0.1:5000/artworks/<int:id>/comments
# This allows a user to make an artwork comment
# WORKING 14/11/22
@artworks.route("/<int:artwork_id>/comments", methods = ["POST"])
@jwt_required()
def create_artwork_comment(artwork_id):
     authorize_user()
     artwork_statement = db.select(Artwork).filter_by(id=artwork_id)
     artwork = db.session.scalar(artwork_statement)
     
     if artwork:
          artwork_comment = ArtworkComment(
               description = request.json['description'],
               date = date.today(),
               user_id = get_jwt_identity(),
               artwork_id = artwork_id
          )
          db.session.add(artwork_comment)
          db.session.commit()
          return ArtworkCommentSchema().dump(artwork_comment), 201
     else:
          return {'error': f"Artwork not found with id '{artwork_id}'"}, 404

# 127.0.0.1:5000/artworks/<int:id>/comments/<int:artwork_comments_id>
# This allows a user to update their comment
# WORKING 14/11/22
@artworks.route("/<int:id>/comments/<int:artwork_comments_id>", methods = ["PUT", "PATCH"])
@jwt_required()
def update_artwork_comment(id, artwork_comments_id):
     artwork_statement = db.select(Artwork).filter_by(id=id)
     artwork = db.session.scalar(artwork_statement)
     artwork_comment_statement = db.select(ArtworkComment).filter_by(id=artwork_comments_id)
     artwork_comment = db.session.scalar(artwork_comment_statement)
     user_id = artwork_comment.user_id
     authorize_precise_user(user_id)
     if artwork and artwork_comment:
          artwork_comment.description = request.json.get('description') or artwork_comment.description
          db.session.commit()
          return ArtworkCommentSchema().dump(artwork_comment)
     elif artwork: 
          return {'error': f"Artwork not found with id {id}"}, 404
     elif artwork_comment:
          return {'error': f"Artwork comment was not found on artwork '{id}'."}, 404


# 127.0.0.1:5000/artworks/<int:id>/comments/<int:artwork_comments_id>
# This allows a user to update their comment
# WORKING 14/11/22
@artworks.route("/<int:id>/comments/<int:artwork_comment_id>", methods = ["DELETE"])
@jwt_required()
def delete_artwork_comment(id, artwork_comment_id):
     artwork_statement = db.select(Artwork).filter_by(id=id)
     artwork = db.session.scalar(artwork_statement)
     artwork_comment_statement = db.select(ArtworkComment).filter_by(id=artwork_comment_id)
     artwork_comment = db.session.scalar(artwork_comment_statement)
     user_id = artwork_comment.user_id
     authorize_precise_user(user_id)
     if artwork and artwork_comment:
          db.session.delete(artwork_comment)
          db.session.commit()
          return {'message': f"Artwork comment '{artwork_comment.description}' deleted successfully"}, 200
     elif artwork: 
          return {'error': f"Artwork Comment not found with id {id}"}, 404
     elif artwork_comment:
          return {'error': f"Artwork was not found on artwork '{id}'."}, 404