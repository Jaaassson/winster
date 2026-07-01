from app.extensions import db, BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)

    products = db.relationship("Product", backref="category", lazy="dynamic")
