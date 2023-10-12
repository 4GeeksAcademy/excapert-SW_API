from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites],
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __table_name__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(10), unique=False, nullable=True)
    eye_color = db.Column(db.String(20), unique=False, nullable=True)
    gender = db.Column(db.String(20), unique=False, nullable=True)
    hair_color = db.Column(db.String(20), unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    mass = db.Column(db.Integer, unique=False, nullable=True)
    skin_color = db.Column(db.String(20), unique=False, nullable=True)
    url = db.Column(db.String(256), unique=False, nullable=True)
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)

    favorites = db.relationship('Favorites', backref='character', lazy=True)

    def __repr__(self):
        return f'<Charaacter {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }

    
    
class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    diameter = db.Column(db.Integer, nullable=True)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    gravity = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(120), nullable=True)
    terrain = db.Column(db.String(120), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String, nullable=True, unique=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)

    favorites = db.relationship('Favorites', backref='planet', lazy=True)

    def __repr__(self):
        return f'<Planet {self.name}>'
    
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }

class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __repr__(self):
        return f'<Favorite {self.id}'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }