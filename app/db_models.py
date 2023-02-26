
from sqlalchemy import Enum
from app import db

class User(db.Model):
    """
        Creates a user table. 
    """
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String, nullable  = False) # nullable prevents from having empty inputs


class Task(db.Model):
    """
        Creates a Task table that is connected to user table with one to many relation (one user, many tasks).
    """
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    title = db.Column(db.String(100), nullable = False) # 100 is max length of input sitnrg
    status = db.Column(Enum('to_do', 'doing', 'done'))

# Initialize database 
db.create_all()
db.session.commit()