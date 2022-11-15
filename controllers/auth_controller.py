from flask import Blueprint, request, abort
from main import db, bcrypt
from datetime import timedelta
from models.users import User, UserSchema
from models.artists import Artist, ArtistSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import date


auth = Blueprint('auth', __name__, url_prefix='/auth')

# 127.0.0.1:5000/auth/user-register
# Register a user to the DB, no auth required.
# WORKING 14/11/22
@auth.route('/user-register', methods=['POST'])
def auth_register_user():
    try:
        user = User(
            user_alias = request.json['email'],
            first_name = request.json.get('first_name'),
            last_name = request.json.get('last_name'),
            join_date = date.today(),
            email = request.json['email'],
            has_subscription = request.json['has_subscription'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude='password').dump(user), 201
    except IntegrityError:
        return {'error': 'Email address or alias already in use'}, 409


# 127.0.0.1:5000/auth/user-register
# Register an artist to the DB, must be admin artist.
# WORKING 14/11/22
@auth.route('/artist-register', methods=['POST'])
@jwt_required()
def auth_register_artist():
    authorize_artist()
    try:
        artist = Artist(
            artreon_alias = request.json["artreon_alias"],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            email = request.json["email"],
            artist_bio = request.json["artist_bio"]
        )
        db.session.add(artist)
        db.session.commit()
        return ArtistSchema(exclude=['password']).dump(artist), 201
    except IntegrityError:
        return {'error': 'Artreon alias or email address already in use'}, 409


# 127.0.0.1:5000/auth/user-login
# Log in a user
# WORKING 14/11/22
@auth.route('/user-login', methods=['POST'])
def auth_user_login():
    user_statement = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(user_statement)

    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=12))
        return {'email': user.email, 'token': token}
    else:
        return {'error': 'The email or password was invalid'}, 404


# Authorize paid user, can view walkthroughs, make comments, view q&as.
# NOT FUNCTIONAL, LEAVING AS ASSIGNMENT DUE.

# def authorize_paid_user():
#     user_id = get_jwt_identity()
#     user_statement = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(user_statement)
#     if not user.has_subscription == False:
#         return abort(401)
    

# Authorize user, users can access viewing artworks, that's basically it.
# BECAUSE OF OTHER FUNCTION WITHDRAWN, ALL USERS HAVE SAME PRIVILEGES.

def authorize_user():
    user_id = get_jwt_identity()
    user_statement = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(user_statement)
    if not user:
        return abort(401)

# Find the right user to update/delete their own comments. 
# WORKING 14/11/22
def authorize_precise_user(id):
    user_id = get_jwt_identity()
    user_statement = db.select(User).filter_by(id=id)
    user = db.session.scalar(user_statement)
    if user.id != int(user_id):
        return abort(401)
    
    # Boilerplate for particular function needing exact user
    # Example is on a comment route
    # user_id = comment_result.user_id
    # authorize_precise_user(user_id)

# 127.0.0.1:5000/auth/artist-login
# Log in an artist
# WORKING 14/11/22
@auth.route('/artist-login', methods=['POST'])
def auth_artist_login():
    artist_statement = db.select(Artist).filter_by(email=request.json['email'])
    artist = db.session.scalar(artist_statement)

    if artist and bcrypt.check_password_hash(artist.password, request.json['password']):

        token = create_access_token(identity=str(artist.id), expires_delta=timedelta(hours=12))
        return {'email': artist.email, 'token': token}
    else:
        return {'error': 'The email or password was invalid'}, 404

# Authorize any artist to do an action on walkthroughs/artworks/q&as.
def authorize_artist():
    artist_id = get_jwt_identity()
    artist_statement = db.select(Artist).filter_by(id=artist_id)
    artist = db.session.scalar(artist_statement)
    if not artist:
        return abort(401)

# Authorize precise artist to perform action on their own id's content.
# DO NOT TOUCH
# WORKING 14/11/22
def authorize_precise_artist(id):
    artist_id = get_jwt_identity()
    artist_statement = db.select(Artist).filter_by(id=id)
    artist = db.session.scalar(artist_statement)
    if artist.id != int(artist_id):
        return abort(401)

    # Boilerplate for particular function needing exact artist
    # Example is on an artwork route
    # artist_id = artwork_result.artist_id
    # authorize_precise_artist(artist_id)