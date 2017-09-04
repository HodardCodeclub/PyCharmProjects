from django.db import models
from mongoengine import *
import datetime

# Create your models here.
class User(Document):
    email = EmailField()
    password = StringField(min_length=8)
    date_modified = DateTimeField(default=datetime.datetime.now)