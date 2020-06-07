from src.db import db
from sqlalchemy import exc
from src.models import Product, Category
import sys

class CategoryProduct(db.Model):
    __tablename__ = "categories_products"
    __table_args__ = (
        db.PrimaryKeyConstraint("category_id", "product_id"),
    )
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    def add_product_categories(self, product_id, categories):
        current_category_ids = list(map(lambda cat: cat.id,
                                    Category.query.filter(Product.id == product_id).all()))

        categories_to_delete = CategoryProduct.query.filter(CategoryProduct.product_id == product_id).filter(CategoryProduct.category_id.in_(current_category_ids))

        categories_to_delete.delete(synchronize_session="fetch")

        if len(categories) > 0:
            db.session().bulk_insert_mappings(
                CategoryProduct,
                [
                    {"category_id": category, "product_id": product_id}
                    for category in categories
                ]
            )

        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] Batch insert product categories " + str(err), sys.stderr)
            return False

        return True
