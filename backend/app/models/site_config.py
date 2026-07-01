from app.extensions import db, BaseModel


class SiteConfig(BaseModel):
    __tablename__ = "site_config"

    id = db.Column(db.Integer, primary_key=True, default=1)
    site_name = db.Column(db.Text)
    site_title = db.Column(db.Text)
    keywords = db.Column(db.Text)
    description = db.Column(db.Text)
    company_name = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    about_us = db.Column(db.Text)
    facebook = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
