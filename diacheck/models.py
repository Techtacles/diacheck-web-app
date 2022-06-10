from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from diacheck import db,login_manager,app
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), unique=False, nullable=False)
    last_name = db.Column(db.String(150), unique=False, nullable=False)
    username = db.Column(db.String(150), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250),unique=False, nullable=False)


    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}','{self.email}')"

class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=False, nullable=False)
    test_number = db.Column(db.Integer, unique=False, nullable=False)
    result = db.Column(db.String(150), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"User('{self.username}', '{self.test_number}','{self.result}')"

