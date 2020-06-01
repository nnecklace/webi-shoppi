from src.models import Base
from src.db import db

class Category(Base):
    __tablename__ = "categories"
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship("Product", secondary="categories_products", back_populates="categories", lazy="joined")
