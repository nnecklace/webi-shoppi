from src.db import db

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship("Product", secondary="categories_products", back_populates="categories", lazy="joined")
