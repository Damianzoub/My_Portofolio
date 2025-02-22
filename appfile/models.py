from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from appfile import db



class USER(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   name  = db.Column(db.String(60),nullable=False)
   email = db.Column(db.String(120),unique=False,nullable=False)
   date = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
   text_area = db.Column(db.Text,nullable=False)

   def __repr__(self):
      return f'User("{self.name}","{self.email})"'


class POST(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   title = db.Column(db.String(60),nullable=False)
   date_posted = db.Column(db.DateTime,nullable = False, default=datetime.utcnow)
   content = db.Column(db.Text,nullable=False)


   def __repr__(self):
       return f"Post('{self.title}','{self.date_posted}','{self.content}')"