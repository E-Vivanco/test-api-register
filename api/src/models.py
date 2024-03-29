from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile = db.relationship("Profile", backref="user", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }
    
    def serialize_profile(self):
        return {
            "id": self.id,
            "email": self.email,
            "biography": self.profile.biography,
            "linkedin": self.profile.linkedin,
            "github": self.profile.github,
            "facebook": self.profile.facebook
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.add(self)


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.String(120), default="")
    linkedin = db.Column(db.String(120), default="")
    github = db.Column(db.String(120), default="")
    facebook = db.Column(db.String(120), default="")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "biopgrafy": self.biography,
            "linkedin": self.linkedin,
            "github": self.github,
            "facebook": self.facebook
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.add(self)
