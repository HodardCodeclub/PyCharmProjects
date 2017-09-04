from django.db import models
from mongoengine import *
import datetime

# Create your models here.
class Account(Document):
    name = StringField()
    password = StringField(min_length=4)
    chapters = ListField(IntField())
    date_modified = DateTimeField(default=datetime.datetime.now)