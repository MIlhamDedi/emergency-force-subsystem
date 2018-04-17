from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from datetime import datetime
import re
db = SQLAlchemy()


class Asset(db.Model):
    """Asset Data Object
    Attributes structure:
        [
            id: int(sequence) !key,
            name: str,
            availability: int
        ]
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    availability = db.Column(db.Integer)

    def __repr__(self):
        return f'<Asset {self.id}){self.name}: {self.availability} available>'

    def convert(self):
        return (self.id, {
            "name": self.name,
            "availability": self.availability
        })


class Plan(db.Model):
    """Plan Data Object
    Data attributes structure:
        [
            id: int(sequence) !key,
            crisis_id: int
            details: str,
            time: datetime.datetime
        ]
    """
    id = db.Column(db.Integer, primary_key=True)
    crisis_id = db.Column(db.Integer)
    details = db.Column(db.String)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'<Plan {self.id}){self.details}>'

    def convert(self):
        return {
            "id": self.id,
            "crisis_id": self.crisis_id,
            "details": self.details,
            "time": str(self.time)
        }


class Report(db.Model):
    """Report Data Object
    Data attributes structure:
        [
            id: int(sequence) !key,
            crisis_id: int,
            assets_used: str -> ((asset_id, number), ...),
            casualty: str -> ((asset_id, number), ...),
            details: str,
            is_final: str,
            time: datetime.datetime
        ]
    """
    id = db.Column(db.Integer, primary_key=True)
    crisis_id = db.Column(db.Integer)
    assets_used = db.Column(db.String)
    casualty = db.Column(db.String)
    details = db.Column(db.String)
    is_final = db.Column(db.Boolean)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f'<Asset {self.id}){self.details}>'

    def convert(self):
        assets_used_parsed = casualty_parsed = ""
        if self.assets_used:
            assets_used_parsed = [(int(a), int(b)) for (a, b) in [
                tuple(c[1:-1].split(','))
                for c in re.findall('[(]\d+,\d+[)]', self.assets_used)
            ]]
        if self.casualty:
            casualty_parsed = [(int(a), int(b)) for (a, b) in [
                tuple(c[1:-1].split(','))
                for c in re.findall('[(]\d+,\d+[)]', self.casualty)
            ]]
        return {
            "id": self.id,
            "crisis_id": self.crisis_id,
            "assets_used": assets_used_parsed,
            "casualty": casualty_parsed,
            "details": self.details,
            "is_final": self.is_final,
            "time": str(self.time)
        }


class User(db.Model):
    """User Instance Class
    Data attributes structure:
        [
            username: str !key,
            pwd_hash: str,
            api_token: str
        ]
    """
    username = db.Column(db.String, primary_key=True)
    pwd_hash = db.Column(db.String, nullable=False)
    api_token = db.Column(db.String)
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def get_id(self):
        return self.username

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
