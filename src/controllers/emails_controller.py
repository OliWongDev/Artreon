from flask import Blueprint, request
from main import db
from models.emails import Email, EmailSchema
from controllers.auth_controller import authorize_artist
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

emails = Blueprint("emails", __name__, url_prefix="/emails")

# 127.0.0.1:5000/emails
# This returns the emails which are made by an artist
# WORKING 14/11/22
@emails.route("/", methods = ["GET"])
# @jwt_required()
def get_all_emails():
    emails_list = db.select(Email).order_by(Email.id.asc())
    result = db.session.scalars(emails_list)
    return EmailSchema(many=True).dump(result)

# 127.0.0.1:5000/emails/<int:id>
# This returns a single email made by the admin artist
# WORKING 14/11/22
@emails.route("/<int:id>", methods=["GET"])
# @jwt_required()
def get_single_email(id):
    email = db.select(Email).filter_by(id=id)
    result = db.session.scalar(email)
    return EmailSchema().dump(result)

# 127.0.0.1:5000/emails
#This allows the admin artist to add an email
# WORKING 14/11/22
@emails.route("/", methods=["POST"])
# @jwt_required()
def add_email():
    # authorize_artist()
    email_fields = EmailSchema().load(request.json)

    new_email = Email(
        email_title = email_fields["email_title"],
        email_content = email_fields["email_content"],
        send_date = date.today(),
        artist_id = 1
    )
    db.session.add(new_email)
    db.session.commit()

    return EmailSchema().dump(new_email), 201