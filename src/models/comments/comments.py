from src.db import db
from src.models import Base

class Comment(Base):
    __tablename__ = "comments"
    content = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    user_id = db.Column(Base.get_user_id_field(), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", passive_deletes=True, lazy="joined")
    # This relation is only used for cascading deletes, sqlalchemy requires backref relation for cascading deletes to work :/
    product = db.relationship("Product", passive_deletes=True, lazy="select")

    def __init__(self, content, product_id, user_id):
        self.content = content
        self.product_id = product_id
        self.user_id = user_id
