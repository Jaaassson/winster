from app.extensions import db, BaseModel


class Inquiry(BaseModel):
    __tablename__ = "inquiry"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)
    is_read = db.Column(db.SmallInteger, default=0)
    is_replied = db.Column(db.SmallInteger, default=0)
    replied_at = db.Column(db.DateTime, nullable=True)

    product = db.relationship("Product", backref="inquiries")
