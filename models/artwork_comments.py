from main import db, ma
from marshmallow import fields

# Artwork Comment Model (SQLAlchemy)
class ArtworkComment(db.Model):

    # Name of the table
    __tablename__ = "artwork_comments"
    
    # Fields that the table takes including constraints.
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date(), nullable=False)

    # Foreign keys included in fields. 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey("artworks.id"), nullable=False)

    # Relationships with other tables. Child to both.
    user = db.relationship("User", back_populates="artwork_comments")
    artwork = db.relationship("Artwork", back_populates="artwork_comments")

# Artwork Comment Schema (Marshmallow)
class ArtworkCommentSchema(ma.Schema):

    # Nested fields structure that are to be added upon with certain artwork comment routes. Only certain information shown.
    user = fields.Nested("UserSchema", only=["id", "user_alias"])
    artwork = fields.Nested("ArtworkSchema", only=["id", "artwork_name"])

    # Meta class that will call the following fields upon route access.
    class Meta:
        fields = ("id", "description", "date", "user", "artwork")
        ordered = True


### AUTHORIZATION ATTEMPT (IGNORE)

# __permissions__ = dict(
#         artist_role=['post', 'read', 'delete'],
#         paid_user_role=['post', 'read', 'delete'],
#         )