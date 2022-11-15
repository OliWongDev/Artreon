# from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin
# from main import db 

# UserGroup = db.Table(
#     'user_group', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('user_group_id', db.Integer, db.ForeignKey('user_groups.id'))
# )

# UserRole = db.Table(
#     'user_role', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('user_role_id', db.Integer, db.ForeignKey('user_groups.id'))
# )

# ArtistGroup = db.Table(
#     'artist_group', db.Model.metadata,
#     db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
#     db.Column('artist_group_id', db.Integer, db.ForeignKey('artist_role.id'))
# )

# ArtistRole = db.Table(
#     'artist_role', db.Model.metadata,
#     db.Column('artist_id', db.Integer, db.ForeginKey('artists.id')),
#     db.Column('artist_role_id'), db.Integer, db.ForeignKey('artist_roles.id')
# )

# class UserGroup(db.Model, RestrictionsMixin):
#     __tablename__ = 'user_groups'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), nullable=False, unique=True)

# class UserRole(db.Model, AllowancesMixin):
#     __tablename__ = 'user_roles'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), nullable=False, unique=True)

# class ArtistGroup(db.Model, RestrictionsMixin):
#     __tablename__ = 'artist_groups'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), nullable=False, unique=True)

# class ArtistRole(db.Model, AllowancesMixin):
#     __tablename__ = 'artist_roles'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), nullable=False, unique=True)