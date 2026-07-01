from app.extensions import db, BaseModel


class Banner(BaseModel):
    __tablename__ = "banner"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.Text)
    button_text = db.Column(db.String(255))
    link_url = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
