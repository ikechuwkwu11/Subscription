from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),unique = True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    subscriptions = db.relationship('Subscription', backref='user', lazy=True)


class Plan(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True,nullable=False)
    price = db.Column(db.Float,nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    billing_cycle = db.Column(db.String(100),nullable=False)
    api_call_limit = db.Column(db.Integer, nullable=False)
    storage_limit_mb = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    subscriptions = db.relationship('Subscription', backref='plan', lazy=True)



    def __str__(self):
        return f'<plan{self.name} - {self.billing_cycle}'

class Subscription(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    plan_id = db.Column(db.Integer,db.ForeignKey('plan.id'),nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)  # can be computed based on billing cycle
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Subscription User {self.user_id} Plan {self.plan_id} Active {self.is_active}>'