from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Relative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.String(32), nullable=True)
    death_date = db.Column(db.String(32), nullable=True)
    photo_url = db.Column(db.String(256), nullable=True)
    father_id = db.Column(db.Integer, db.ForeignKey('relative.id'), nullable=True)
    mother_id = db.Column(db.Integer, db.ForeignKey('relative.id'), nullable=True)
    children = db.relationship('Relative', backref=db.backref('parents', remote_side=[id]), primaryjoin=db.or_(id==father_id, id==mother_id))