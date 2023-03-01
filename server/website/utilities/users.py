from flask_login import UserMixin


class User(UserMixin):
    """ User class that is initialised when a user is loaded i.e. logs-in
        Attributes can be accessed via current_user.attribute when a user
        is logged in
    """

    def __init__(self, user_id, username, password,
                 topics=[], watched_videos=["", "", ""], channels=[]):
        self.authenticated = False
        self.id = user_id
        self.username = username
        self.password = password
        self.watched_videos = watched_videos
        self.topics = topics
        self.channels = channels

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
