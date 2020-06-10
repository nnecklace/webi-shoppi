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
        curr_product = Product.query.get(product_id)

        if not curr_product:
            return False

        categories = list(map(lambda cat: int(cat), categories))

        # delete the categories not selected in update
        CategoryProduct.query \
                       .filter(CategoryProduct.product_id == product_id) \
                       .filter(CategoryProduct.category_id.notin_(categories)) \
                       .delete(synchronize_session="fetch")

        # everytime we access the property categories a query is made
        # this is why we save it in a variable
        curr_categories = list(map(lambda cat: cat.id, curr_product.categories))

        if len(categories) > 0:
            db.session().bulk_insert_mappings(
                CategoryProduct,
                [
                    {"category_id": category, "product_id": product_id}
                    for category in [cat for cat in categories if cat not in curr_categories]
                ]
            )

        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] Batch insert product categories " + str(err), sys.stderr)
            return False

        return True
