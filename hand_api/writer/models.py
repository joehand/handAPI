from ..extensions import db
from ..utils import mongo_to_dict
from ..user import User

from datetime import datetime

class Post(db.Document):
    user_ref = db.ReferenceField(User)
    url = db.StringField(unique=True, required=True)
    content = db.StringField()
    kind = db.StringField(choices=('Daily', 'Blog', 'Link'), required=True)
    last_update = db.DateTimeField(default=datetime.now(), required=True)

    meta = {'allow_inheritance': True}

    def to_dict(self):
        return mongo_to_dict(self)

class DailyPost(Post):
    date = db.DateTimeField(default=datetime.now(), required=True)

class BlogPost(Post):
    title = db.StringField()
    kind = db.StringField(default='blog')
    published = db.BooleanField(default=False, required=True)
    pub_date = db.DateTimeField(required=True)

    def clean(self):
        """Ensures that published essays have a `pub_date` """
        if self.published and self.pub_date is None:
            self.pub_date = datetime.now()

class LinkPost(BlogPost):
    kind = db.StringField(default='link')
    link_url = db.StringField()
