import time

from sven.db.model import Model
from sven.db.field import StringField,BooleanField, FloatField
from sven.utils import util


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=util.generate_id, column_type='varchar(50)')
    email = StringField(column_type='varchar(50)')
    passwd = StringField(column_type='varchar(50)')
    admin = BooleanField()
    name = StringField(column_type='varchar(50)')
    image = StringField(column_type='varchar(500)')
    created_at = FloatField(default=time.time)
