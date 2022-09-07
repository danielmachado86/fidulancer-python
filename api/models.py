import re
import mongoengine as me
from api import db


class User(db.Document):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    username = me.StringField(required=True, regex=re.compile('^[\w]{8,25}$'))
    email = me.EmailField(required=True)
    password = me.StringField(required=True, regex=re.compile('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=]).{8,25}$'))