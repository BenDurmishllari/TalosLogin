from Talos import db, app, route, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    surname = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
   

    # methods that manage the expire of secret token
    # genarate and serialize this key that it't unique for any user
    # def get_reset_token(self, expires_sec = 600):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    

    #printed method ToString()
    def __repr__(self):
        return f"Users('{self.id}','{self.name}', '{self.surname},'{self.email}'')"
