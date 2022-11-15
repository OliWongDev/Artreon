from controllers.artists_controller import artists
from controllers.artworks_controller import artworks
from controllers.auth_controller import auth
from controllers.emails_controller import emails
from controllers.q_and_as_controller import q_and_as
from controllers.users_controller import users
from controllers.walkthroughs_controller import walkthroughs

registerable_controllers = [
    artists,
    artworks,
    auth,
    emails,
    q_and_as,
    users,
    walkthroughs
]