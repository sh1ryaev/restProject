from utils.db_api.db_commands import create_dish
import asyncio
from utils.db_api.database import create_db


async def create_dishes():
    #Закуски
    await create_dish(name="Фокачча с тапенадом",
                      category_name="🥪Закуски", category_code="snack",
                      price=650, description="Домашняя итальянская лепешка с чесноком, розмарином и морской солью с "
                                             "тапенадом из маслин и высушенных на солнце томатов",
                      photo="https://static.tildacdn.com/tild3265-6666-4632-b635-386433343661/-072.JPG")
    await create_dish(name="Фокачча с рикоттой",
                      category_name="🥪Закуски", category_code="snack",
                      price=620, description="Домашняя итальянская лепешка с чесноком, розмарином и морской солью с "
                                             "рикоттой и лимоном",
                      photo="https://eda.yandex/images/1380157/3e5815e247faaec9be3bab9e34ad1340-450x300.jpeg")
    await create_dish(name="Брускетта с рикоттой и томатами",
                   category_name="🥪Закуски", category_code="snack",
                   price=420, description="Хрустящая чиабатта с муссом из рикотты и вялеными томатами",
                   photo="https://tdk-maslo.ru/images/com_yoorecipe/5/cropped-Br-t.jpg")
    await create_dish(name="Брускетта с паштетом",
                   category_name="🥪Закуски", category_code="snack",
                   price=420, description="Хрустящая чиабатта с паштетом из куриной печени, бальзамического уксуса и пармезана",
                   photo="https://s1.eda.ru/StaticContent/Photos/130805160644/190731180823/p_O.jpg")
    #Салаты
    await create_dish(name="Салат Цезарь с курицей",
                   category_name="🥗Салаты", category_code="salad",
                   price=690, description="Классика",
                   photo="https://www.gastronom.ru/binfiles/images/20191113/b50e9f2a.jpg")
    await create_dish(name="Салат с грушей и горгонзолой",
                   category_name="🥗Салаты", category_code="salad",
                   price=660, description="Салат с грушей, сыром горгонзола, грецким орехом и соусе на основе сливок и сыра горгонзола",
                   photo="https://images11.domashnyochag.ru/upload/img_cache/458/45867e85660b5a7fa11ccec5cb0b6d12_ce_460x460x0x0_cropped_666x444.jpg")
    await create_dish(name="Тартар из лосося",
                   category_name="🥗Салаты", category_code="salad",
                   price=960, description="Тартар из лосося с кремом из авокадо",
                   photo="https://kulinarissimo.com/uploads/img/full/b90e1bc0c1ee47da64ee6d7269005642.jpg")
    await create_dish(name="Тартар из говядины",
                   category_name="🥗Салаты", category_code="salad",
                   price=960, description="Тартар из говядины с каперсом и желтком",
                   photo="https://e1.edimdoma.ru/data/posts/0002/3407/23407-ed4_wide.jpg?1631182636")
    #Супы
    await create_dish(name="Суп Pappa Al Pomodoro",
                   category_name="🍲Супы", category_code="soup",
                   price=460, description="Суп из сладких томатов, чеснока, базилика, с добавлением хлеба и оливкового масла",
                   photo="https://www.gastronom.ru/binfiles/images/20151231/bab7d352.jpg")
    await create_dish(name="Крем-суп грибной",
                   category_name="🍲Супы", category_code="soup",
                   price=460, description="Деревенски грибной крем-суп со сливками и хрустящими крутонами из хлеба",
                   photo="https://img.povar.ru/main/1f/bc/c0/0b/sirnii_krem-sup_s_shampinonami-317448.jpg")
    await create_dish(name="Суп с морепродуктами",
                   category_name="🍲Супы", category_code="soup",
                   price=1140, description="Томатный суп с филе трески, креветками, кальмаром, мини осьминогами, мидиями, томатами черри, базиликом и чили",
                   photo="https://www.gastronom.ru/binfiles/images/20170201/bbe34c7e.jpg")
    await create_dish(name="Куриный суп с пастой фрегола",
                   category_name="🍲Супы", category_code="soup",
                   price=420, description="Цветная капуста, брокколи, паста фрегола, курица, морковь",
                   photo="https://new-magazine.ru/wp-content/uploads/2020/10/IL-Letterato_Tykvenyy-sup-s-gorgonzolloy.jpg")
    #Пицца
    await create_dish(name="Пицца Маргарита",
                   category_name="🍕Пицца", category_code="pizza",
                   price=580, description="Томатный соус с базиликом, моцарелла и оливковое масло",
                   photo="https://km-doma.ru/assets/gallery_thumbnails/31/319484a4bb725e4eacab62c7f0c7f1ed.jpg")
    await create_dish(name="Пицца Парма",
                   category_name="🍕Пицца", category_code="pizza",
                   price=840, description="Прошутто ди парма, томаты, базилик, руккола, пармезан, моцарелла",
                   photo="https://tuttopizza.ru/image/cache/catalog/product/pizza-parma-rukkola-900x600.jpg")
    await create_dish(name="Пицца 4 Сыра",
                   category_name="🍕Пицца", category_code="pizza",
                   price=690, description="Моцарелла, горгонзола, гауда, скаморца и свежая руккола",
                   photo="https://static.1000.menu/img/content-v2/12/4a/15419/italyanskaya-picca-4-syra-v-duxovke_1589476545_19_max.jpg")
    await create_dish(name="Пицца с грушей и горгонзолой",
                   category_name="🍕Пицца", category_code="pizza",
                   price=720, description="Груша, соус бешамель, горгонзола, моцарелла, грецкий орех",
                   photo="https://italiani.rest/upload/resize_cache/iblock/3b5/450_450_2/3b5451f6c6d7daf0f2141b4b8c91519b.jpg")
    #Паста
    await create_dish(name="Лингвини с креветками",
                   category_name="🍝Паста", category_code="pasta",
                   price=1040, description="Лингвини с томатным соусом и креветками",
                   photo="https://s1.eda.ru/StaticContent/Photos/120213181135/120213181457/p_O.jpg")
    await create_dish(name="Тальолини с копченой форелью",
                   category_name="🍝Паста", category_code="pasta",
                   price=960, description="Тальолии в сливочном соусе, с копченой форелью и вешенками",
                   photo="https://storage.ginzadelivery.ru/product/37499/l.80cb0ab85fae755eeaafd65844858cd3.jpg")
    await create_dish(name="Домашняя запеченная лазанья",
                   category_name="🍝Паста", category_code="pasta",
                   price=790, description="Лазанья с соусами бешамель и болоньезе, на основе свиного и говяжьего фарша",
                   photo="https://s1.eda.ru/StaticContent/Photos/160312155529/160320211135/p_O.jpg")
    await create_dish(name="Феттучине с грибами",
                   category_name="🍝Паста", category_code="pasta",
                   price=790, description="Феттучине с шампиньонами и грибным соусом на основе белых грибов и сыра маскарпоне",
                   photo="https://halal-spb.ru/sites/default/files/styles/large/public/fetuchini-s-gribami.jpg?itok=Ccd9hQnw")
    #Напитки
    await create_dish(name="Вода негазированная",
                   category_name="🥤Напитки", category_code="drinks",
                   price=190, description="0.5 л.",
                   photo="https://static.detmir.st/media_out/694/176/3176694/1500/0.jpg?1559698226139")
    await create_dish(name="Fanta",
                   category_name="🥤Напитки", category_code="drinks",
                   price=190, description="0.5 л.",
                   photo="https://kantanello.ru/wp-content/uploads/2017/05/%D1%84%D0%B0%D0%BD%D1%82%D0%B0-05.jpg")
    await create_dish(name="Sprite",
                   category_name="🥤Напитки", category_code="drinks",
                   price=190, description="0.5 л.",
                   photo="https://static.tildacdn.com/tild6137-6239-4533-b230-653036623539/_1.jpg")
    await create_dish(name="Coca-cola",
                   category_name="🥤Напитки", category_code="drinks",
                   price=190, description="0.5 л.",
                   photo="https://cornelipizza.ru/upload/iblock/df8/df8dd98899de3c4878e218d9467e327f.JPG")

loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(create_dishes())
