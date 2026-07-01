from app.extensions import db, BaseModel


class Product(BaseModel):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    model = db.Column(db.String(100))  # 型号
    description = db.Column(db.Text)
    images = db.Column(db.Text)
    specs = db.Column(db.Text)
    price_usd = db.Column(db.Float, default=0)
    price_cny = db.Column(db.Float, default=0)
    stock = db.Column(db.Integer, default=0)
    moq = db.Column(db.Integer, default=1)
    packaging = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_hot = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.SmallInteger, default=1)
