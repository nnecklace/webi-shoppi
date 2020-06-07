from src.db import db
from src.models import Base
from sqlalchemy.dialects.postgresql import UUID
from src.constants import env_sqlite
from sqlalchemy import exc, text
import sys

class Product(Base):
    __tablename__ = "products"
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=0)

    id_field = None
    if not env_sqlite():
        id_field = UUID(as_uuid=True)
    else:
        id_field = db.Integer

    user_id = db.Column(id_field, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", passive_deletes=True, back_populates="products", lazy="joined")
    categories = db.relationship("Category", secondary="categories_products", back_populates="products", lazy="joined")

    def __init__(self, name, price, quantity, user_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.user_id = user_id

    def _commit(self, err_log):
        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] " + err_log + " " + str(err), sys.stderr)
            return False

        return True

    def save(self):
        db.session().add(self)
        return self._commit("product create:")

    def update(self, product):
        self.name = product.name.data
        self.price = product.price.data
        self.quantity = product.quantity.data
        return self._commit("product " + str(self.id) + " update :")

    def delete(self):
        db.session().delete(self)
        return self._commit("product " + str(self.id) + " delete :")

    @staticmethod
    def find_by_criteria(name, categories, price, minimum, published_start, published_end, seller):
        params_dict = {}

        stmt = ("SELECT products.id,"
               " products.name,"
               " products.created_at,"
               " products.price,"
               " products.quantity,"
               " users.username"
               " FROM products"
               " LEFT JOIN categories_products"
               " ON categories_products.product_id = products.id"
               " LEFT JOIN categories"
               " ON categories.id = categories_products.category_id"
               " INNER JOIN users"
               " ON users.id = products.user_id"
               " WHERE products.quantity > 0")

        date_format_start = "%Y-%m-%d 00:00:00"
        date_format_end  = "%Y-%m-%d 23:59:59"

        def build_query(key, value = ""):
            nonlocal stmt
            if key == "name":
                stmt += " AND products.name LIKE :name"
            elif key == "price":
                stmt += " AND products.price <= :price"
            elif key == "minimum":
                stmt += " AND products.price = (SELECT MIN(products.price) FROM products)"
            elif key == "seller":
                stmt += " AND users.username LIKE :seller"
            elif key == "published_start":
                stmt +=  " AND products.created_at >= :published_start"
            elif key == "published_end":
                stmt +=  " AND products.created_at <= :published_end"
            elif key == "order_by":
                stmt += " ORDER BY products.created_at DESC"
            elif key == "group_by":
                stmt += " GROUP BY products.id, users.username"
            elif key == "categoryless":
                stmt += " HAVING COUNT(categories_products.product_id) = 0"

            if value:
                params_dict[key] = value

        if name:
            build_query("name", "%"+name+"%")

        if price and not minimum:
            build_query("price", price)

        if minimum:
            build_query("minimum")

        # Could also use SQL BETWEEN clause, but doing it this way makes to code easier to read imo
        if published_start:
            build_query("published_start", published_start.strftime(date_format_start))

        if published_end:
            build_query("published_end", published_end.strftime(date_format_end))

        if seller:
            build_query("seller", "%"+seller+"%")

        if not -1 in categories and len(categories) > 0:
            # build subquery for getting categories
            subquery = " AND categories.id = ANY(SELECT categories.id FROM categories WHERE categories.id = :cat_0"
            build_query("cat_0", categories[0])
            for indx in range(1, len(categories)):
                subquery += " OR categories.id = :cat_"+str(indx)
                build_query("cat_"+str(indx), categories[indx])
            subquery += ")"
            stmt += subquery

        build_query("group_by")

        # if uncategorized was selected
        if -1 in categories:
            build_query("categoryless")
        
        build_query("order_by")

        stmt = text(stmt).bindparams(**params_dict)

        rows = db.engine.execute(stmt)
        response = []
        lookup = []

        for row in rows:
            if not row[0] in lookup:
                response.append({"id": row[0],
                                "name": row[1],
                                "created_at": row[2],
                                "price": row[3],
                                "quantity": row[4],
                                "user": {"username": row[5]}})
                lookup.append(row[0])

        return response
