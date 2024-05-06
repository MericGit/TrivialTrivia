from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username =  db.StringField(unique=True, required=True,min_length=1,max_length=40)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()
    high_score = db.IntField(default=0)
    questions_seen = db.IntField(default=0)
    questions_correct = db.IntField(default=0)
    # Returns unique string identifying our object
    def get_id(self):
        return self.username
    def load_user(user_id):
        return User.objects(username=user_id).first()

class Question(db.Document):
    creator = db.ReferenceField(User)
    question = db.StringField(unique=True, required=True,min_length=5,max_length=1000)
    answer = db.StringField(unique=True, required=True,min_length=1,max_length=100)
    category = db.StringField(required=True)