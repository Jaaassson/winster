from app.extensions import db, BaseModel


class News(BaseModel):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
