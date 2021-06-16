from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), nullable=True)
    surname = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
         "id": self.id,
         "username": self.username,
         "name": self.name,
         "surname": self.surname
        }

    def __repr__(self):
        return f"ID - {self.id} . Username - {self.username}"



