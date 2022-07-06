from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.db_commands import read_dishes, read_categories, read_dish, read_basket

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "category", "item_id","buy","clear","delete","add")
buy_item = CallbackData("buy", "item_id")
create_order = CallbackData("create_order","id_bas")
basket_cd=CallbackData("show_bas","bas_id")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="0", item_id="0", buy="0", clear="0", delete="0", add="0"):
    return menu_cd.new(level=level, category=category, item_id=item_id, buy=buy,
                       clear=clear, delete=delete, add=add)


def make_callback_order(id_bas):
    return create_order.new(id_bas=id_bas)


# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def categories_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=2)

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    categories = await read_categories()
    for category in categories:
        # Чекаем в базе сколько товаров существует под данной категорией
        # Сформируем текст, который будет на кнопке
        button_text = f"{category.category_name}"

        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)

        # Вставляем кнопку в клавиатуру

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
        text=f"🛒 Корзина",
        callback_data=make_callback_data(level=3))
    )

    # Возвращаем созданную клавиатуру в хендлер
    return markup





# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def items_keyboard(category):
    CURRENT_LEVEL = 1

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
    markup = InlineKeyboardMarkup(row_width=2)

    # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
    items = await read_dishes(category)
    for item in items:
        # Сформируем текст, который будет на кнопке
        button_text = f"{item.name} - {item.price}₽"

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           item_id=item.id)
        markup.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text=f"🛒 Корзина",
            callback_data=make_callback_data(level=3))
    )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 1 - на выбор подкатегории
    markup.row(
        InlineKeyboardButton(
            text="⬅Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
def item_keyboard(category, item_id):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"🛒 Добавить в заказ",
            callback_data=make_callback_data(item_id=item_id, level=3, buy=1)
        )
    )
    return markup


# Создаем функцию, которая отдает корзину с кнопками "Оформить заказ" и "назад" для выбранного товара
async def basket_keyboard(category, bas_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    basket = await read_basket(bas_id)
    for product_in_basket in basket:
        item = await read_dish(product_in_basket.id_prod)
        # Сформируем текст, который будет на кнопке
        button_text = f"{item.name} - {item.price}₽"

        # Сформируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           item_id=item.id)
        markup.row(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )
        cancel = InlineKeyboardButton(
            text="-",
            callback_data=make_callback_data(level=CURRENT_LEVEL, delete=1, item_id=item.id))
        redact = InlineKeyboardButton(
            text='+',
            callback_data=make_callback_data(level=CURRENT_LEVEL, add=1, item_id=item.id))
        kolvo = InlineKeyboardButton(
            text=f"{product_in_basket.kolvo}",
            callback_data=make_callback_data(level=CURRENT_LEVEL))
        markup.row(cancel)
        markup.insert(kolvo)
        markup.insert(redact)
    markup.row(
        InlineKeyboardButton(
            text=f"Очистить корзину",
            callback_data=make_callback_data(level=CURRENT_LEVEL, clear=1))
        )
    markup.row(
        InlineKeyboardButton(
            text=f"Оформить заказ",
            callback_data=make_callback_order(id_bas=0))
    )
    markup.row(
        InlineKeyboardButton(
            text=f"⬅Назад",
            callback_data=make_callback_data(level=0))
    )
    return markup
