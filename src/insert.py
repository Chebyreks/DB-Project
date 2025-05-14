from sqlalchemy import select, schema

from db.models import *
from db.data_creation import *

url = "postgresql+psycopg2://{user}:{password}@{host}/{database}" # ЗАПОЛНИТЬ !!!!!!

engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}/{database}") # ЗАПОЛНИТЬ !!!!!!

schema_name = "shop"
conn = engine.connect().execution_options(
    schema_translate_map={None: schema_name})
conn.execute(schema.CreateSchema(schema_name, if_not_exists=True))
conn.commit()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
conn.close()

with Session(engine) as session:
    users = generate_users()
    session.add_all(users)
    session.commit()
    
    categories = generate_categories()
    session.add_all(categories)
    session.commit()
    
    goods = generate_goods(categories)
    session.add_all(goods)
    session.commit()
    
    carts = generate_shopping_carts(users)
    session.add_all(carts)
    session.commit()
    
    s = select(Good)
    goods = session.execute(s).all()
    cart_goods = generate_cart_goods(carts, goods)
    session.add_all(cart_goods)
    session.commit()
    
    vehicles = generate_delivery_vehicles()
    session.add_all(vehicles)
    session.commit()
    
    agents = generate_delivery_agents(vehicles)
    session.add_all(agents)
    session.commit()
    
    orders = generate_orders(carts, agents, session)
    session.add_all(orders)
    session.commit()
    
    logs = generate_vehicle_logs(vehicles, agents)
    session.add_all(logs)
    session.commit()
