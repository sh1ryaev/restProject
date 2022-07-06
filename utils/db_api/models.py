from sqlalchemy import (Column, Integer, String, Sequence, Date)
from sqlalchemy import sql
from utils.db_api.database import db


class Dish(db.Model):
    __tablename__ = 'dishes'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    category_code = Column(String(50))
    category_name = Column(String(50))
    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)
    description = Column(String(250))


class Basket(db.Model):
    __tablename__ = 'bskts'
    query: sql.Select
    id_bas = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    id = Column(Integer)
    id_prod = Column(Integer)
    price = Column(Integer)
    kolvo = Column(Integer)


# Создаем класс пользователя
class Customer(db.Model):
    __tablename__ = 'cust'
    query: sql.Select
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    user_id = Column(String(50))
    name = Column(String(50))
    phone = Column(String(12))
    address = Column(String(250))


class Table(db.Model):
    __tablename__='tables'
    query: sql.Select
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    kolvo_person = Column(Integer)
    is_free = Column(Integer)


class BookingTable(db.Model):
    __tablename__='booking_tables'
    query: sql.Select
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(String(50))
    table_id = Column(Integer)
    date = Column(String(10))


class SostavOrder(db.Model):
    __tablename__ = 'sos_orders'
    query: sql.Select
    id = Column(Integer)
    id_user = Column(String(50))
    id_prod = Column(Integer)
    price = Column(Integer)
    kolvo = Column(Integer)

class Order(db.Model):
    __tablename__ = 'ord'
    query: sql.Select
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    id_user = Column(String(50))
    order_date = Column(Date)
    summa = Column(Integer)
    payment_type = Column(String(50))
    address = Column(String(250))