import random
from datetime import datetime, timedelta
from faker import Faker
from db.models import *
from sqlalchemy import select

fake = Faker('ru_RU')

def generate_users(num=10):
    users = []
    for _ in range(num):
        first_name = fake.first_name().lower()
        last_name = fake.last_name().lower()
        account_name = f"{first_name}_{last_name}"
        email = f"{first_name}.{last_name}@example.com"
        phone = f"+7{random.randint(1000000000, 9999999999)}"
        bonus = random.randint(0, 300)
        users.append(User(account_name=account_name, email=email, phone_number=phone, bonus_credits=bonus))
    return users

def generate_shopping_carts(users):
    carts = []
    for user in users:
        account_name = user.account_name
        carts.append(ShoppingCart(user_name=account_name, active=True))
        if random.random() > 0.3:
            carts.append(ShoppingCart(user_name=account_name, active=False))
    return carts

def generate_categories():
    categories = [
        'Электроника', 'Одежда', 'Обувь', 'Продукты питания', 'Косметика',
        'Товары для дома', 'Игрушки', 'Спортивные товары', 'Автотовары', 'Книги',
        'Мебель', 'Товары для детей', 'Товары для животных', 'Канцтовары', 'Бытовая химия'
    ]
    categories_res = []
    for category in categories:
        categories_res.append(Category(name=category))
    return categories_res

def generate_goods(categories):
    
    # Как это иначе сделать можно????
    
    goods = [
        Good(category_id=1, name='Телевизор Samsung 50"', price=30000, amount_in_stock=50),
        Good(category_id=1, name='Смартфон iPhone 13', price=75000, amount_in_stock=30),
        Good(category_id=1, name='Ноутбук HP Pavilion', price=55000, amount_in_stock=20),
        Good(category_id=1, name='Наушники Sony WH-1000XM4', price=15000, amount_in_stock=100),
        Good(category_id=1, name='Камера Canon EOS 90D', price=85000, amount_in_stock=10),
        
        Good(category_id=2, name='Футболка Nike', price=2000, amount_in_stock=100),
        Good(category_id=2, name='Джинсы Levis', price=6000, amount_in_stock=50),
        Good(category_id=2, name='Куртка Columbia', price=12000, amount_in_stock=30),
        Good(category_id=2, name='Рубашка Ralph Lauren', price=4000, amount_in_stock=80),
        Good(category_id=2, name='Платье Zara', price=3000, amount_in_stock=120),
        
        Good(category_id=3, name='Кроссовки Adidas Ultraboost', price=8000, amount_in_stock=60),
        Good(category_id=3, name='Ботинки Timberland', price=10000, amount_in_stock=40),
        Good(category_id=3, name='Сандалии Birkenstock', price=4000, amount_in_stock=150),
        Good(category_id=3, name='Кеды Converse Chuck Taylor', price=3500, amount_in_stock=80),
        Good(category_id=3, name='Туфли Giorgio Armani', price=15000, amount_in_stock=25),
        
        Good(category_id=4, name='Хлеб ржаной', price=50, amount_in_stock=500),
        Good(category_id=4, name='Молоко 1 литр', price=80, amount_in_stock=1000),
        Good(category_id=4, name='Куриное филе', price=250, amount_in_stock=200),
        Good(category_id=4, name='Яблоки', price=120, amount_in_stock=150),
        Good(category_id=4, name='Картофель', price=60, amount_in_stock=300),
        
        Good(category_id=5, name='Тушь Maybelline', price=800, amount_in_stock=200),
        Good(category_id=5, name='Помада MAC', price=1500, amount_in_stock=150),
        Good(category_id=5, name='Крем для лица Nivea', price=600, amount_in_stock=100),
        Good(category_id=5, name='Парфюм Chanel No. 5', price=10000, amount_in_stock=20),
        Good(category_id=5, name='Шампунь Head & Shoulders', price=300, amount_in_stock=300),
        
        Good(category_id=6, name='Пылесос Samsung', price=10000, amount_in_stock=40),
        Good(category_id=6, name='Микроволновая печь LG', price=6000, amount_in_stock=30),
        Good(category_id=6, name='Чайник Philips', price=2000, amount_in_stock=100),
        Good(category_id=6, name='Утюг Tefal', price=3000, amount_in_stock=70),
        Good(category_id=6, name='Стиральная машина Bosch', price=25000, amount_in_stock=15),
        
        Good(category_id=7, name='Плюшевый мишка', price=1500, amount_in_stock=100),
        Good(category_id=7, name='Конструктор Lego', price=3500, amount_in_stock=50),
        Good(category_id=7, name='Кубики', price=500, amount_in_stock=200),
        Good(category_id=7, name='Кукла Barbie', price=2500, amount_in_stock=150),
        Good(category_id=7, name='Трек для машинок Hot Wheels', price=1500, amount_in_stock=120),
        
        Good(category_id=8, name='Гантели 5 кг', price=1500, amount_in_stock=80),
        Good(category_id=8, name='Роликовые коньки', price=3500, amount_in_stock=60),
        Good(category_id=8, name='Йога-коврик', price=800, amount_in_stock=120),
        Good(category_id=8, name='Фитнес-браслет Xiaomi', price=2500, amount_in_stock=100),
        Good(category_id=8, name='Теннисная ракетка Wilson', price=4500, amount_in_stock=40),
        
        Good(category_id=9, name='Автомобильные чехлы', price=2000, amount_in_stock=60),
        Good(category_id=9, name='Автокресло Cybex', price=12000, amount_in_stock=20),
        Good(category_id=9, name='Компрессор для авто', price=3000, amount_in_stock=80),
        Good(category_id=9, name='Шампунь для авто', price=500, amount_in_stock=200),
        Good(category_id=9, name='Сигнализация для автомобиля', price=15000, amount_in_stock=10),
        
        Good(category_id=10, name='Роман "1984" Джордж Оруэлл', price=500, amount_in_stock=300),
        Good(category_id=10, name='Блокнот Moleskine', price=1500, amount_in_stock=120),
        Good(category_id=10, name='Книга "Мастер и Маргарита"', price=700, amount_in_stock=150),
        Good(category_id=10, name='Атлас мира', price=1000, amount_in_stock=200),
        Good(category_id=10, name='Словарь иностранных слов', price=800, amount_in_stock=100)
    ]
    return goods

def generate_cart_goods(carts, goods):
    cart_goods = []
    for cart_id in range(1, len(carts)+1):
        num_items = random.randint(1, 9)
        selected_goods = random.sample(goods, num_items)
        for good in selected_goods:
            good_id = good[0].good_id
            price_with_discount = int(good[0].price)
            amount = random.randint(1, 3)
            cart_goods.append(CartGood(shopping_cart_id=cart_id, good_id=good_id, price_with_discount=price_with_discount, amount=amount))
    return cart_goods

def generate_delivery_vehicles():
    vehicles = []
    types = ['Автомобиль', 'Велосипед', 'Самокат']
    addresses = ['ул. Транспортная, д. 1', 'ул. Пушкина, д. 5', 'ул. Карла Маркса, д. 30']
    
    for _ in range(8):
        vehicle = random.choice(types)
        address = random.choice(addresses)
        vehicles.append(DeliveryVehicle(vehicle=vehicle, vacant=False, storage_address=address))
    
    for _ in range(7):
        vehicle = random.choice(types)
        address = random.choice(addresses)
        vehicles.append(DeliveryVehicle(vehicle=vehicle, vacant=True, storage_address=address))
    
    return vehicles

def generate_delivery_agents(vehicles):
    agents = []
    for _ in range(5):
        name = fake.first_name()
        surname = fake.last_name()
        agents.append(DeliveryAgent(vehicle_id=None, name=name, surname=surname, active =True))

    occupied_vehicles = set()
    available_vehicles = [v for v in vehicles if not v.vacant and v.delivery_id not in occupied_vehicles]
    for _ in range(2):
        if not available_vehicles:
            break 
        vehicle = random.choice(available_vehicles)
        occupied_vehicles.add(vehicle.delivery_id)
        available_vehicles.remove(vehicle)
        name = fake.first_name()
        surname = fake.last_name()
        agents.append(DeliveryAgent(vehicle_id=vehicle.delivery_id, name=name, surname=surname, active =True))

    for i in range(6):
        vehicle = random.choice(available_vehicles)
        occupied_vehicles.add(vehicle.delivery_id)
        available_vehicles.remove(vehicle)
        name = fake.first_name()
        surname = fake.last_name()
        agents.append(DeliveryAgent(vehicle_id=vehicle.delivery_id, name=name, surname=surname, active =False))

    return agents

def generate_orders(carts, agents, session):
    orders = []
    cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск', 'Казань']

    for cart_id in range(1, len(carts)+1):
        cart_goods = session.execute(select(CartGood).where(CartGood.shopping_cart_id==cart_id))
        agent_id = random.choice([a.agent_id for a in agents if a.active])
        if agent_id is None:
            continue
            
        city = random.choice(cities)
        street = fake.street_name()
        address = f"{city}, {street}, д. {random.randint(1, 100)}"
        
        total_price = sum([cart_good[0].price_with_discount for cart_good in cart_goods])
        spent_bonus = 0
        
        orders.append(Order(shopping_cart_id=cart_id, agent_id=agent_id, delivery_address=address, total_price=total_price, spent_bonus_credits=spent_bonus))

    return orders

def generate_vehicle_logs(vehicles, agents):
    logs = []
    active_agents_with_vehicles = [
        agent for agent in agents 
        if agent.active and agent.vehicle_id is not None
    ]
    
    for agent in active_agents_with_vehicles:
        time_start = fake.date_time_between(start_date='-30d', end_date='now')
        logs.append(DeliveryVehicleLog(
            vehicle_id=agent.vehicle_id,
            agent_id=agent.agent_id,
            time_start=time_start,
            time_stop=None
        ))
        
    for agent in random.sample(agents, k = random.randint(0, len(agents))):
        for vehicle in random.sample(vehicle, k=random.randint(1, 2)):
            num_logs = random.randint(3, 5)
            for _ in range(num_logs):
                vehicle = random.choice(vehicles)
                time_start = fake.date_time_between(start_date='-1y', end_date='-30d')
                usage_duration = timedelta(days=random.randint(7, 28))
                time_stop = time_start + usage_duration
                logs.append(DeliveryVehicleLog(
                    vehicle_id=vehicle.delivery_id,
                    agent_id=agent.agent_id,
                    time_start=time_start,
                    time_stop=time_stop
                ))
            
    return logs