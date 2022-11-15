from src.main import db, ma
from marshmallow import fields

# QAndAComment Model (SQLAlchemy)
class QAndAComment(db.Model):

    # Name of table
    __tablename__ = "q_and_a_comments"
    
    # Fields exclusive to Q&A Comment Model, constraints administered.
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date())

    # Foreign keys that map the user who created the Q&A comment, and the comment to the particular Q&A
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    q_and_a_id = db.Column(db.Integer, db.ForeignKey("q_and_as.id"), nullable=False)

    # Relationships mapped. Q&A Comment is a child of both user and Q&A
    user = db.relationship("User", back_populates="q_and_a_comments")
    q_and_a = db.relationship("QAndA", back_populates="q_and_a_comments")

# Q&A Comment Schema (Marshmallow)    
class QAndACommentSchema(ma.Schema):
    
    # Nested fields providing context for the user and what Q&A the comment was made to. Information filtered to be relevant.
    user = fields.Nested("UserSchema", only=["id", "user_alias"])
    q_and_a = fields.Nested("QAndASchema", only=["id"])

    # Meta class detailing what fields are shown in a route request.
    class Meta:
        fields = ("id", "description", "date", "user", "q_and_a")
        ordered = True

### AUTHORIZATION ATTEMPT (IGNORE)

# __permissions__= dict(
    #     artist_role=["read"],
    #     paid_user_role=["read", "delete", "post", "update"]
    # )