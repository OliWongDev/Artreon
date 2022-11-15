from src.main import db, ma
from marshmallow import fields

# Email Model (SQLAlchemy)
class Email(db.Model):
    
    # Name of table
    __tablename__ = "emails"
        
    # Fields exclusive to emails table. Constraints administered here.
    id = db.Column(db.Integer, primary_key=True)
    email_title = db.Column(db.String(), nullable=False, unique=True)
    email_content = db.Column(db.Text, nullable=False)
    send_date = db.Column(db.Date())

    # Foreign key linking to the artist that posted the artwork.
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)

    # Relationship to Artist logged here. Emails is a child to the artist who posted it.
    artist = db.relationship("Artist", back_populates="emails")

# Email Schema (Marshmallow)
class EmailSchema(ma.Schema):

    # Artist field nested to provide author context to a potential email posted.
    artist = fields.Nested("ArtistSchema", only=["id", "artreon_alias"])

    # Meta class listing fields when a route for an email is called.
    class Meta:
        fields = ("id", "email_title", "email_content", "send_date", "artist")
        ordered = True

### AUTHORIZATION ATTEMPT (IGNORE)

# __permissions__= dict(
#         artist_role=['read', 'post'],
#         paid_user_role=['read'],
#         free_user_role=['read'])