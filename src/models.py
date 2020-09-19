from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
db = SQLAlchemy()

# Class table for USER
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False, default='')
    last_name = db.Column(db.String(80), unique=False, nullable=False, default='')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    zipcode = db.Column(db.String(10), unique=False, nullable=False)
    sex = db.Column(db.String(10), unique=False, nullable=False)
    type_of_user = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "zipcode": self.zipcode,
            "sex": self.sex,
            "type_of_user": self.type_of_user
        }

# Class table for JOB POST
class Job_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(1000), unique=False, nullable=False)
    job_description = db.Column(db.String(2000), unique=False, nullable=False)
    job_address = db.Column(db.String(120), unique=False, nullable=False)
    job_state = db.Column(db.String(120), unique=False, nullable=False)
    job_city = db.Column(db.String(120), unique=False, nullable=False)
    job_zipcode = db.Column(db.String(10), unique=False, nullable=False)
    job_payment = db.Column(db.String(10), unique=False, nullable=False)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self): 
        return '<Job_Post %r>' % self.job_title

    def serialize(self):
        return {
            "id": self.id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "job_address": self.job_address,
            "job_state": self.job_state,
            "job_city": self.job_city,
            "job_zipcode": self.job_zipcode,
            "job_payment": self.job_payment,
        }