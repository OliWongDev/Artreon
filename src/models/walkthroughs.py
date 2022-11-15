from main import db, ma
from marshmallow import fields

# Walkthrough Model (SQLAlchemy)
class Walkthrough(db.Model):
    
    # Name of table
    __tablename__ = "walkthroughs"

    # Exclusive fields to walkthroughs. Constraints administered.
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    date = db.Column(db.Date(), nullable=False)

    # Foreign keys relating the walkthrough to the artist who made it, and the artwork it is about.
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey("artworks.id"), nullable=False)

    # Relations mapped to walkthrough. A walkthrough is a child to the artist who created it and the artwork it derives from.
    # But is a child to the walkthrough comments made on it.
    artist = db.relationship("Artist", back_populates="walkthroughs")
    artwork = db.relationship("Artwork", back_populates="walkthrough")
    walkthrough_comments = db.relationship("WalkthroughComment", back_populates="walkthrough", cascade="all, delete")

# Walkthrough Schema (Marshmallow)
class WalkthroughSchema(ma.Schema):

    # Nested fields for a walkthrough. Filtered information such as the artist who created it, the artwork it is about and what comments have been made on it.
    artist = fields.Nested("ArtistSchema", only=["artreon_alias"])
    artwork = fields.Nested("ArtworkSchema", only=["id", "artwork_name"])
    walkthrough_comments = fields.List(fields.Nested("WalkthroughCommentSchema", only=["id", "description", "user.user_alias"]))

    # Meta class disclosing the nested fields on a walkthrough route request.
    class Meta:
        fields = ("id", "description", "date", "artist", "artwork", "walkthrough_comments")
        ordered = True


### AUTHORIZATION ATTEMPT (IGNORE)

# __permissions__ = dict(
#         artist_role=["read", "update", "post", "delete"],
#         paid_user_role=["read"]
#     )