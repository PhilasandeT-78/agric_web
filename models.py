from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    survey_responses = db.relationship('Survey', backref='user', lazy=True)
    field_horticultural_crops = db.relationship('FieldHorticulturalCrops', backref='user', lazy=True)
    demographics = db.relationship('Demographic', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Demographic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registered_name = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    municipality = db.Column(db.String(100), nullable=False)
    agricultural_activity = db.Column(db.String(255), nullable=False)
    other_agricultural_activity = db.Column(db.String(255))
    farm_activity = db.Column(db.String(255))

    def __repr__(self):
        return (f"Demographic('{self.id}', '{self.user_id}', '{self.registered_name}', "
                f"'{self.province}', '{self.district}', "
                f"'{self.municipality}', '{self.agricultural_activity}', "
                f"'{self.other_agricultural_activity}', '{self.farm_activity}')")

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crops_own = db.Column(db.Numeric, nullable=False, default=0)
    crops_govt = db.Column(db.Numeric, nullable=False, default=0)
    crops_traditional = db.Column(db.Numeric, nullable=False, default=0)
    crops_other = db.Column(db.Numeric, nullable=False, default=0)
    pastures_own = db.Column(db.Numeric, nullable=False, default=0)
    pastures_govt = db.Column(db.Numeric, nullable=False, default=0)
    pastures_traditional = db.Column(db.Numeric, nullable=False, default=0)
    pastures_other = db.Column(db.Numeric, nullable=False, default=0)
    greenhouses_own = db.Column(db.Numeric, nullable=False, default=0)
    greenhouses_govt = db.Column(db.Numeric, nullable=False, default=0)
    greenhouses_traditional = db.Column(db.Numeric, nullable=False, default=0)
    greenhouses_other = db.Column(db.Numeric, nullable=False, default=0)
    natural_forest_own = db.Column(db.Numeric, nullable=False, default=0)
    natural_forest_govt = db.Column(db.Numeric, nullable=False, default=0)
    natural_forest_traditional = db.Column(db.Numeric, nullable=False, default=0)
    natural_forest_other = db.Column(db.Numeric, nullable=False, default=0)
    woodland_own = db.Column(db.Numeric, nullable=False, default=0)
    woodland_govt = db.Column(db.Numeric, nullable=False, default=0)
    woodland_traditional = db.Column(db.Numeric, nullable=False, default=0)
    woodland_other = db.Column(db.Numeric, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return (f"Survey('{self.id}', '{self.user_id}', "
                f"crops_own='{self.crops_own}', crops_govt='{self.crops_govt}', "
                f"crops_traditional='{self.crops_traditional}', crops_other='{self.crops_other}', "
                f"pastures_own='{self.pastures_own}', pastures_govt='{self.pastures_govt}', "
                f"pastures_traditional='{self.pastures_traditional}', pastures_other='{self.pastures_other}', "
                f"greenhouses_own='{self.greenhouses_own}', greenhouses_govt='{self.greenhouses_govt}', "
                f"greenhouses_traditional='{self.greenhouses_traditional}', greenhouses_other='{self.greenhouses_other}', "
                f"natural_forest_own='{self.natural_forest_own}', natural_forest_govt='{self.natural_forest_govt}', "
                f"natural_forest_traditional='{self.natural_forest_traditional}', natural_forest_other='{self.natural_forest_other}', "
                f"woodland_own='{self.woodland_own}', woodland_govt='{self.woodland_govt}', "
                f"woodland_traditional='{self.woodland_traditional}', woodland_other='{self.woodland_other}', "
                f"timestamp='{self.timestamp}')")

class FieldHorticulturalCrops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    farming_practice = db.Column(db.String(255), nullable=False)
    water_supply = db.Column(db.String(255), nullable=False)
    irrigation_system = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return (f"FieldHorticulturalCrops('{self.id}', '{self.user_id}', "
                f"farming_practice='{self.farming_practice}', water_supply='{self.water_supply}', "
                f"irrigation_system='{self.irrigation_system}', timestamp='{self.timestamp}')")





