from ..extensions import db
from ..utils import mongo_to_dict
from ..user import User

from datetime import datetime

class Post(db.Document):
    user_ref = db.ReferenceField(User)
    content = db.StringField()
    last_update = db.DateTimeField(default=datetime.utcnow, required=True)
    date = db.StringField(default=datetime.today().strftime('%d-%b-%Y'), required=True)

    def to_dict(self):
        return mongo_to_dict(self)
