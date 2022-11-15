from main import db, ma
from marshmallow import fields

# Walkthrough Comment Model (SQLAlchemy)
class WalkthroughComment(db.Model):

    # Name of table
    __tablename__ = "walkthrough_comments"
    
    # Exclusive fields of a walkthrough comment with constraints.
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date())

    # Foreign keys mapping the comment to the user and what walkthrough it was on.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    walkthrough_id = db.Column(db.Integer, db.ForeignKey("walkthroughs.id"), nullable=False)

    # Relations to a user and walkthrough. A walkthrough comment is a child to both user and walkthrough.
    user = db.relationship("User", back_populates="walkthrough_comments")
    walkthrough = db.relationship("Walkthrough", back_populates="walkthrough_comments")

# Walkthrough Comment Schema (Marshmallow)
class WalkthroughCommentSchema(ma.Schema):

    # A walkthrough comment is nested with what user made the comment, and what walkthrough it is attributed to.
    user = fields.Nested("UserSchema", only=["id", "user_alias"])
    walkthrough = fields.Nested("WalkthroughSchema", only=["id", "description"])

    # Meta class detailing the fields that are returned in a route request.
    class Meta:
        fields = ("id", "description", "date", "user", "walkthrough")
        ordered = True

# AUTHORIZATION ATTEMPT (IGNORE)

# __permissions__ = dict(
#         artist_role=["read"],
#         paid_user_role=["post", "read", "update", "delete"]