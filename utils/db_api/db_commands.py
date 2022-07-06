from typing import List
from sqlalchemy import and_
from utils.db_api.models import Dish, Basket, Customer, Order, SostavOrder, Table, BookingTable
from utils.db_api.database import db


async def create_dish(**kwargs):
    new_dish = await Dish(**kwargs).create()
    return new_dish


async def create_customer(**kwargs):
    new_cus = await Customer(**kwargs).create()
    return new_cus


async def create_new_order(**kwargs):
    new_order = await Order(**kwargs).create()
    return new_order


async def create_sostav_order(**kwargs):
    new_order = await SostavOrder(**kwargs).create()
    return new_order


async def read_sostav_order(id):
    orders = await SostavOrder.query.where(SostavOrder.id == id).gino.all()
    return orders


async def read_order(id_user):
    orders = await Order.query.where(Order.id_user == id_user).gino.all()
    return orders


async def read_customer(id_user):
    cus = await Customer.query.where(Customer.user_id == id_user).gino.first()
    print()
    return cus


async def add_dish_in_basket(**kwargs):
    add_basket = await Basket(**kwargs).create()
    return add_basket


async def del_dish_in_basket(id, id_prod):
    dishes = await Basket.query.where(Basket.id == id).gino.all()
    itm = dishes[0]
    for i in dishes:
        if i.id_prod == id_prod:
            itm = i
    dish = await Basket.query.where(Basket.id_bas == itm.id_bas).gino.first()
    del_basket = await Basket.delete.where(Basket.id_bas == dish.id_bas).gino.status()
    return del_basket


async def delete_basket(id):
    del_basket = await Basket.delete.where(Basket.id == id).gino.status()
    return del_basket


async def plus_basket(id, dish_id):
    dishes = await Basket.query.where(Basket.id == id).gino.all()
    itm=dishes[0]
    for i in dishes:
        if i.id_prod==dish_id:
            itm=i
    kolvo=itm.kolvo+1
    dish = await Basket.query.where(Basket.id_bas == itm.id_bas).gino.first()
    return await Basket.update.values(kolvo=kolvo).where(Basket.id_bas == dish.id_bas).gino.status()


async def change_name(user_id,name):
    customer = await Customer.query.where(Customer.user_id == user_id).gino.first()
    cus = await Customer.query.where(Customer.id == customer.id).gino.first()
    return await Customer.update.values(name=name).where(Customer.id == cus.id).gino.status()


async def change_phone(user_id,phone):
    customer = await Customer.query.where(Customer.user_id == user_id).gino.first()
    cus = await Customer.query.where(Customer.id == customer.id).gino.first()
    return await Customer.update.values(phone=phone).where(Customer.id == cus.id).gino.status()


async def change_address(user_id,address):
    customer = await Customer.query.where(Customer.user_id == user_id).gino.first()
    cus = await Customer.query.where(Customer.id == customer.id).gino.first()
    return await Customer.update.values(address=address).where(Customer.id == cus.id).gino.status()


async def minus_basket(id, dish_id):
    dishes = await Basket.query.where(Basket.id == id).gino.all()
    itm = dishes[0]
    for i in dishes:
        if i.id_prod == dish_id:
            itm = i
    kolvo = itm.kolvo
    dish = await Basket.query.where(Basket.id_bas == itm.id_bas).gino.first()
    if dish.kolvo>1:
        kolvo=dish.kolvo-1
        return await Basket.update.values(kolvo=kolvo).where(
            Basket.id_bas == dish.id_bas).gino.status()
    else:
        await del_dish_in_basket(id, dish_id)


async def read_basket(bas_id):
    return await Basket.query.where(Basket.id == bas_id).gino.all()


async def read_categories() -> List[Dish]:
    return await Dish.query.distinct(Dish.category_name).gino.all()


async def read_dishes(category_code) -> List[Dish]:
    dishes = await Dish.query.where(Dish.category_code == category_code).gino.all()
    return dishes


async def read_dish(dish_id) -> Dish:
    dish = await Dish.query.where(Dish.id == dish_id).gino.first()
    return dish


#tables
async def read_free_tables(date):
    tables = await Table.query.gino.all()
    booking = await BookingTable.query.where(BookingTable.date==date).gino.all()
    if len(booking)>0:
        for table in tables:
            for b in booking:
                if table.id==b.table_id:
                      table.is_free=1
    return tables


async def read_tables():
    tables = await Table.query.gino.all()
    return tables


async def create_tables(**kwargs):
    new_table = await Table(**kwargs).create()
    return new_table


#booking_tables
async def read_booking_tables(user_id):
    book_tables = await BookingTable.query.where(BookingTable.user_id==user_id).gino.all()
    return book_tables


async def create_booking_tables(**kwargs):
    new_table = await BookingTable(**kwargs).create()
    return new_table


async def delete_booking(table_id, date):
    del_booking = await BookingTable.query.where(
        and_(BookingTable.table_id == int(table_id),
             BookingTable.date == date)
    ).gino.first()
    del_b = await BookingTable.delete.where(BookingTable.id == del_booking.id).gino.status()
    return del_b
