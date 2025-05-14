from datetime import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, 
    DateTime, ForeignKey, Numeric
)
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "shop"}

    account_name = Column(String(50), primary_key=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20))
    bonus_credits = Column(Integer, default=0)

    shopping_carts = relationship("ShoppingCart", back_populates="user")

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    __table_args__ = {"schema": "shop"}
    
    shopping_cart_id = Column(Integer, primary_key=True, autoincrement="auto")
    user_name = Column(String(50), ForeignKey('shop.users.account_name'), nullable=False)
    active = Column(Boolean, default=True)

    user = relationship("User", back_populates="shopping_carts")
    cart_goods = relationship("CartGood", back_populates="shopping_cart")
    order = relationship("Order", back_populates="shopping_cart", uselist=False)

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {"schema": "shop"}
    
    category_id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(50), unique=True, nullable=False)

    goods = relationship("Good", back_populates="category")

class Good(Base):
    __tablename__ = 'goods'
    __table_args__ = {"schema": "shop"}
    
    good_id = Column(Integer, primary_key=True, autoincrement="auto")
    category_id = Column(Integer, ForeignKey('shop.categories.category_id'), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    amount_in_stock = Column(Integer, default=0)

    category = relationship("Category", back_populates="goods")
    cart_goods = relationship("CartGood", back_populates="good")

class CartGood(Base):
    __tablename__ = 'cart_goods'
    __table_args__ = {"schema": "shop"}
    
    cart_goods_id = Column(Integer, primary_key=True, autoincrement="auto")
    shopping_cart_id = Column(Integer, ForeignKey('shop.shopping_carts.shopping_cart_id'), nullable=False)
    good_id = Column(Integer, ForeignKey('shop.goods.good_id'), nullable=False)
    price_with_discount = Column(Numeric(10, 2), nullable=False)
    amount = Column(Integer, default=1)

    shopping_cart = relationship("ShoppingCart", back_populates="cart_goods")
    good = relationship("Good", back_populates="cart_goods")

class DeliveryVehicle(Base):
    __tablename__ = 'delivery_vehicle'
    __table_args__ = {"schema": "shop"}
    
    delivery_id = Column(Integer, primary_key=True, autoincrement="auto")
    vehicle = Column(String(50), nullable=False)
    vacant = Column(Boolean, default=True)
    storage_address = Column(String(200))

    agents = relationship("DeliveryAgent", back_populates="vehicle")
    vehicle_logs = relationship("DeliveryVehicleLog", back_populates="vehicle")

class DeliveryAgent(Base):
    __tablename__ = 'delivery_agent'
    __table_args__ = {"schema": "shop"}
    
    agent_id = Column(Integer, primary_key=True, autoincrement="auto")
    vehicle_id = Column(Integer, ForeignKey('shop.delivery_vehicle.delivery_id'), nullable=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)

    vehicle = relationship("DeliveryVehicle", back_populates="agents")
    orders = relationship("Order", back_populates="agent")
    vehicle_logs = relationship("DeliveryVehicleLog", back_populates="agent")

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {"schema": "shop"}
    
    order_id = Column(Integer, primary_key=True, autoincrement="auto")
    shopping_cart_id = Column(Integer, ForeignKey('shop.shopping_carts.shopping_cart_id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('shop.delivery_agent.agent_id'))
    delivery_address = Column(String(200), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    spent_bonus_credits = Column(Integer, default=0)

    shopping_cart = relationship("ShoppingCart", back_populates="order")
    agent = relationship("DeliveryAgent", back_populates="orders")
    
class DeliveryVehicleLog(Base):
    __tablename__ = 'delivery_vehicle_log'
    __table_args__ = {"schema": "shop"}
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    vehicle_id = Column(Integer, ForeignKey('shop.delivery_vehicle.delivery_id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('shop.delivery_agent.agent_id'), nullable=False)
    time_start = Column(DateTime, nullable=False, default=datetime.utcnow)
    time_stop = Column(DateTime)

    vehicle = relationship("DeliveryVehicle", back_populates="vehicle_logs")
    agent = relationship("DeliveryAgent", back_populates="vehicle_logs")