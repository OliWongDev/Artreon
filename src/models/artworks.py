from src.main import db, ma
from marshmallow import fields

# Artwork Model (SQLAlchemy)
class Artwork(db.Model):
    
    # Name of table
    __tablename__ = "artworks"
    
    # Fields exclusive to the artworks table. Constraints included.
    id = db.Column(db.Integer, primary_key=True)
    artwork_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String())
    date = db.Column(db.Date(), nullable=False)

    # Foreign key to the artist that it was made by.
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    # Relations to other tables. Parent to artwork_comments and walkthrough. Child to artist.
    artist = db.relationship("Artist", back_populates="artworks")
    artwork_comments = db.relationship("ArtworkComment", back_populates="artwork", cascade="all, delete")
    walkthrough = db.relationship("Walkthrough", back_populates="artwork", cascade="all, delete", uselist=False)

# Artwork Schema (Marshmallow)
class ArtworkSchema(ma.Schema):

    # Nesting the relational data to be accessed by calling the artworks route. Information filtered to be relevant for the route path.
    artist = fields.Nested('ArtistSchema', only=["id", "artreon_alias"])
    artwork_comments = fields.List(fields.Nested('ArtworkCommentSchema', only=["id", "description", "user.user_alias"]))
    walkthrough = fields.Nested("WalkthroughSchema", only=["id"])

    # Meta class containing the fields that are to be listed on the schema if a request is made.
    class Meta:
        fields = ("id", "artwork_name", "description", "date", "artist", "artwork_comments", "walkthrough")
        ordered = True


# AUTHORIZATION ATTEMPT (IGNORE)

# __permissions__ = dict(
    #     artist_role=['post', 'read', 'delete', 'update'],
    #     paid_user_role=['read'],
    #     free_user_role=['read']
    #     )