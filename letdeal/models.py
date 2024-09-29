import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from letdeal import db,login_manager



class User(db.Model,UserMixin):
    __tablename__ = 'users'
        
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    #password_hash = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20),unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"User({self.name},{self.email},{self.phone},{self.updated_at})"
    
    def get_id(self):
        return str(self.user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    street = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    #type = db.Column(db.String(50))  # e.g., Home, Office

    user = db.relationship('User', backref=db.backref('addresses', lazy=True))

    def __repr__(self):
        return f"Address({self.street},{self.city},{self.state},{self.postal_code})"

class Seller(db.Model):
    __tablename__ = 'sellers'

    seller_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    factory_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    requirement = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('seller', lazy=True))

    def __repr__(self):
        return f"Seller({self.factory_name},{self.description},{self.requirement})"

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    # parent_category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'))
                            
    # parent_category = db.relationship('Category', remote_side=[category_id])

    def __repr__(self):
        return f"Category({self.category_id},{self.name})"

class Product(db.Model):
    __tablename__ = 'products'
        
    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Seller_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sellers.seller_id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'))
    #brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey('brands.brand_id'))
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    seller = db.relationship('Seller', backref=db.backref('sellers', lazy=True))
    #brand = db.relationship('Brand', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f"Product({self.name},{self.description},{self.price},{self.stock_quantity})"


class Order(db.Model):
    __tablename__ = 'orders'
        
    order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='Pending')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('addresses.address_id'))
    billing_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sellers.seller_id'))
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    shipping_address = db.relationship('Address', foreign_keys=[shipping_address_id])
    billing_address = db.relationship('Seller', foreign_keys=[billing_address_id])


class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    
    order_item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'))
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return f"OrderItem({self.product_id},{self.quantity},{self.price_at_purchase})"