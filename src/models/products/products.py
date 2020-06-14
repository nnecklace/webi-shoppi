from src.db import db
from src.models import Base
from sqlalchemy import text
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    user_id = db.Column(Base.get_user_id_field(), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", passive_deletes=True, back_populates="products", lazy="joined")
    categories = db.relationship("Category", secondary="categories_products", back_populates="products", lazy="joined", order_by="asc(Category.name)")
    comments = db.relationship("Comment", passive_deletes=True, back_populates="product", lazy="joined")

    def __init__(self, name, price, quantity, user_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.user_id = user_id

    def update(self, product):
        self.name = product.name.data
        self.price = product.price.data
        self.quantity = product.quantity.data
        return self._commit("product " + str(self.id) + " update :")

    @staticmethod
    def find_by_criteria(name, categories, price, minimum, published_start, published_end, seller):
        params_dict = {}
        date_format_start = "%Y-%m-%d 00:00:00"
        date_format_end  = "%Y-%m-%d 23:59:59"

        commands = {
            "quantity"        : " WHERE products.quantity > 0",
            "name"            : " AND LOWER(products.name) LIKE :name",
            "price"           : " AND products.price <= :price",
            "seller"          : " AND LOWER(users.username) LIKE :seller",
            "published_start"  : " AND products.created_at >= :published_start",
            "published_end"   : " AND products.created_at <= :published_end",
            "group_by"        : " GROUP BY products.id, users.username",
            "categoryless"    : " HAVING COUNT(categories_products.product_id) = 0",
            "order_by"        : " ORDER BY products.created_at DESC",
            "categories_join" : (" LEFT JOIN categories_products"
                                 " ON categories_products.product_id = products.id"
                                 " LEFT JOIN categories"
                                 " ON categories.id = categories_products.category_id"),
            "seller_join"     : " INNER JOIN users ON users.id = products.user_id",
            "minimum_start"   : " WHERE products.price = (SELECT MIN(products.price) FROM products",
            "categories_start": " AND categories.id IN (SELECT categories.id FROM categories",
            "category_where"  : " WHERE categories.id = ",
            "category_or"     : " OR categories.id = ",
            "subquery_end"    : ")"
        }

        stmt = ("SELECT products.id,"
               " products.name,"
               " products.created_at,"
               " products.price,"
               " products.quantity,"
               " users.username"
               " FROM products"
               " INNER JOIN users"
               " ON users.id = products.user_id")

        def build_query(key, value = "", extra = None):
            nonlocal stmt
            if key in commands:
                stmt += commands[key]
                if extra:
                    stmt += ":"+value

            if value:
                if extra:
                    params_dict[value] = extra
                else:
                    params_dict[key] = value

        if len(categories) > 0 and not minimum:
            build_query("categories_join")

        if minimum:
            build_query("minimum_start")
            if seller:
                build_query("seller_join")
            if len(categories) > 0:
                build_query("categories_join")

        build_query("quantity")

        if price and not minimum:
            build_query("price", price)

        if name:
            build_query("name", "%"+name.lower()+"%")

        # Could also use SQL BETWEEN clause, but doing it this way makes to code easier to read imo
        if published_start:
            build_query("published_start", published_start.strftime(date_format_start))

        if published_end:
            build_query("published_end", published_end.strftime(date_format_end))

        if seller:
            build_query("seller", "%"+seller.lower()+"%")

        if not -1 in categories and len(categories) > 0:
            # build subquery for getting categories
            build_query("categories_start")
            build_query("category_where", "cat_0", categories[0])
            for indx in range(1, len(categories)):
                build_query("category_or", "cat_"+str(indx), categories[indx])
            build_query("subquery_end")

        # if uncategorized was selected
        if -1 in categories:
            build_query("group_by")
            build_query("categoryless")

        if minimum:
            build_query("subquery_end")

        build_query("order_by")

        stmt = text(stmt).bindparams(**params_dict)

        rows = db.engine.execute(stmt)
        response = []
        lookup = []

        for row in rows:
            if not row[0] in lookup:
                response.append({"id": row[0],
                                "name": row[1],
                                "created_at": datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S") if type(row[2]) is str else row[2],
                                "price": row[3],
                                "quantity": row[4],
                                "user": {"username": row[5]}})
                lookup.append(row[0])

        return response
