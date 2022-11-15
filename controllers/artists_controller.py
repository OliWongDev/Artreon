from flask import Blueprint, request
from main import db
from models.artists import Artist, ArtistSchema
from controllers.auth_controller import authorize_user, authorize_precise_artist
from flask_jwt_extended import jwt_required



artists = Blueprint('artists', __name__, url_prefix="/artists")


# 127.0.0.1:5000/artists
# This returns all Artists on the Graphic God Artreon.
# WORKING 14/11/22
@artists.route("/", methods=["GET"])
@jwt_required()
def get_all_artists():
    artist_list = db.select(Artist).order_by(Artist.id.asc())
    result = db.session.scalars(artist_list)
    if result:
        return ArtistSchema(many=True, exclude=["password"]).dump(result), 200
    else:
        return {"error": f"No artists exist in the database."}, 404


# 127.0.0.1:5000/artists/<int:id>
# This returns a single artist's information and their content.
# WORKING 14/11/22
@artists.route("/<int:id>", methods=["GET"])

@jwt_required()
def get_one_artist(id):
    artist = db.select(Artist).filter_by(id=id)
    result = db.session.scalar(artist)
    if result:
        return ArtistSchema(exclude=["password"]).dump(result), 200
    else:
        return {"error": f"The artist with the id '{id}' was not found"}, 404


# 127.0.0.1:5000/artists/<str:artreon_alias>
# This allows you to grab an artist by their alias
# WORKING 14/11/22
@artists.route("/<string:artreon_alias>", methods=["GET"])
@jwt_required()
def get_artist_by_alias(artreon_alias):
    artist = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    result = db.session.scalar(artist)
    if result:
        return ArtistSchema(exclude=["password"]).dump(result), 200
    else:
        return {"error": f"The artist with the id '{id}' was not found"}, 404

# 127.0.0.1:5000/artists/<str:artreon_alias>
# This allows the artist to update their details
# WORKING 14/11/22
@artists.route("/<string:artreon_alias>", methods=["PUT", "PATCH"])
@jwt_required()
def update_artist_details(artreon_alias):
    artist_data = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    artist = db.session.scalar(artist_data)
    artist_id = artist.id
    authorize_precise_artist(artist_id)
    if artist:
        artist.artreon_alias = request.json.get("artreon_alias") or artist.artreon_alias
        artist.password = request.json.get("password") or artist.password
        artist.email = request.json.get("email") or artist.email
        artist.artist_bio = request.json.get("artist_bio") or artist.artist_bio
        return ArtistSchema(exclude=["password"]).dump(artist)
    else:
        return {"error": f"The artist with the artreon alias'{artreon_alias}' was not found"}, 404

# 127.0.0.1:5000/artists/<str:artreon_alias>
# This deletes the artist by their artreon alias
# WORKING 14/11/22
@artists.route("/<string:artreon_alias>", methods=["DELETE"])
@jwt_required()
def delete_artist_account(artreon_alias):
    artist_statement = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    artist = db.session.scalar(artist_statement)
    artist_id = artist.id
    authorize_precise_artist(artist_id)
    if artist:
        db.session.delete(artist)
        db.session.commit()
        return {'message': f"The user '{artreon_alias}' was deleted successfully"}
    else:
        return {"error": f"The artist with the name {artreon_alias} was not found to be deleted."}, 404

# 127.0.0.1:5000/artists/<str:artreon_alias>/artworks
# This gets the artworks made by the artist if not found returns a 404.
# WORKING 14/11/22
@artists.route("/<string:artreon_alias>/artworks", methods=["GET"])
@jwt_required()
def get_all_artist_artworks(artreon_alias):
    artist_statement = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    artist = db.session.scalar(artist_statement)
    if artist and artist.artworks:
        return ArtistSchema(only=("artreon_alias", "artworks")).dump(artist), 200
    elif artist:
        return {"error": f"No artwork found for artist '{artreon_alias}'"}, 404
    else:
        return {"error": f"The artist with the artreon alias'{artreon_alias}' was not found"}, 404

# 127.0.0.1:5000/artists/<str:artreon_alias>/walkthroughs
# This gets the walkthroughs made by the artist if not found returns a 404.
# WORKING 14/11/22
@artists.route("/<string:artreon_alias>/walkthroughs", methods=["GET"])
@jwt_required()
def get_all_artist_walkthroughs(artreon_alias):
    artist_statement = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    artist = db.session.scalar(artist_statement)
    authorize_user()
    if artist and artist.walkthroughs:
        return ArtistSchema(only=["artreon_alias", "walkthroughs"]).dump(artist), 200
    elif artist:
        return {"error": f"No walkthrough found for artist '{artreon_alias}'"}, 404
    else:
        return {"error": f"The artist with the artreon alias'{artreon_alias}' was not found"}, 404

# 127.0.0.1:5000/artists/<str:artreon_alias>/emails
# WORKING 14/11/22
# JWT required
@artists.route("/<string:artreon_alias>/emails", methods=["GET"])
@jwt_required()
def get_all_artist_emails(artreon_alias):
    artist_statement = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    artist = db.session.scalar(artist_statement)
    authorize_user()
    if artist and artist.emails:
        return ArtistSchema(only=["artreon_alias", "emails"]).dump(artist), 200
    elif artist:
        return {"error": f"No email found for artist '{artreon_alias}'"}, 404
    else:
        return {"error": f"The artist with the artreon alias'{artreon_alias}' was not found"}, 404

# 127.0.0.1:5000/artists/<str:artreon_alias>/qandas
# This returns all qandas made by an artist.
# WORKING 14/11/22

@artists.route("/<string:artreon_alias>/qandas", methods=["GET"])
@jwt_required()
def get_all_artist_q_and_as(artreon_alias):
    artist_statement = db.select(Artist).filter_by(artreon_alias=artreon_alias)
    artist = db.session.scalar(artist_statement)
    authorize_user()
    if artist and artist.q_and_as:
        return ArtistSchema(only=["artreon_alias", "q_and_as"]).dump(artist), 200
    elif artist:
        return {"error": f"No Q&A found for artist '{artreon_alias}'"}, 404
    else:
        return {"error": f"The artist with the artreon alias'{artreon_alias}' was not found"}, 404

