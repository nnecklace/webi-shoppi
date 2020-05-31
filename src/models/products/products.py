from src.db import db
from src.models.base import Base
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

    user_id = db.Column(id_field, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="products", lazy="joined")
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
    def find_by_criteria(name, categories, price, published_start, published_end, seller):
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

        if name:
            stmt += " AND products.name LIKE :name"
            params_dict["name"] = "%"+name+"%"

        if price:
            stmt += " AND price <= :price"
            params_dict["price"] = price

        if published_start and published_end:
            stmt += " AND products.created_at BETWEEN :published_start AND :published_end"
            params_dict["published_start"] = published_start.strftime("%Y-%m-%d 00:00:00")
            params_dict["published_end"] = published_end.strftime("%Y-%m-%d 23:59:59")
        elif published_start:
            stmt +=  " AND products.created_at >= :published_start"
            params_dict["published_start"] = published_start.strftime("%Y-%m-%d 00:00:00")
        elif published_end:
            stmt +=  " AND products.created_at <= :published_end"
            params_dict["published_end"] = published_end.strftime("%Y-%m-%d 23:59:59")

        if seller:
            stmt += " AND users.username LIKE :seller"
            params_dict["seller"] = "%"+seller+"%"

        if -1 in categories:
            stmt += " GROUP BY products.id, users.username"
            stmt += " HAVING COUNT(categories_products.product_id) = 0"
        elif len(categories) > 0:
            subquery = " AND categories.id = ANY(SELECT categories.id FROM categories WHERE categories.id = :cat_0"
            params_dict["cat_0"] = categories[0]
            for indx in range(1, len(categories)):
                subquery += " OR categories.id = :cat_"+str(indx)
                params_dict["cat_"+str(indx)] = categories[indx]
            subquery += ")"
            stmt += subquery
            stmt += " GROUP BY products.id, users.username"

        stmt += " ORDER BY products.created_at DESC"

        stmt = text(stmt).bindparams(**params_dict)

        rows = db.engine.execute(stmt)
        response = []

        for row in rows:
            response.append({"id": row[0],
                             "name": row[1],
                             "created_at": row[2],
                             "price": row[3],
                             "quantity": row[4],
                             "user": {"username": row[5]}})

        return response
