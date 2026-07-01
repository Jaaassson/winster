from app.extensions import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(BaseModel):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
