from main import db, ma
from marshmallow import fields

# Q&A Model (SQLAlchemy)
class QAndA(db.Model):

    # Name of table
    __tablename__ = "q_and_as"
   
    # Fields exclusive to Q&A. Constraints given.
    id = db.Column(db.Integer, primary_key=True)
    q_and_a_content = db.Column(db.String(), nullable=False, unique=True)
    date = db.Column(db.Date(), nullable=False)

    # Foreign key linking the Q&A to the artist id of who made the Q&A
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

    # Relation to artist and q_and_a_comments. Q&A is a parent to Q&A comments, but is a child to the artist who made it.
    artist = db.relationship("Artist", back_populates="q_and_as")
    q_and_a_comments = db.relationship("QAndAComment", back_populates="q_and_a", cascade="all, delete")

# Q&A Schema (Marshmallow)
class QAndASchema(ma.Schema):

    # Nested information that is relevant to the Q&A such as who made it, and what comments are on that particular Q&A.
    artist = fields.Nested("ArtistSchema", only=["id", "artreon_alias"])
    q_and_a_comments = fields.List(fields.Nested("QAndACommentSchema", only=["id", "description", "user.user_alias"]))

    # Meta class listing all the fields that will show on a route request.
    class Meta:
        fields = ("id", "q_and_a_content", "date", "artist", "q_and_a_comments")
        ordered = True


### AUTHORIZATION ATTEMPT (IGNORE)

#  __permissions__ = dict(
#         artist_role=["read", "post", "update", "delete"],
#         paid_user_role=["read"],