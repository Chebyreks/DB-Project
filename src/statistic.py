from db.models import *
from db.data_creation import *

import pandas as pd
import numpy as np

import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash import Dash, dcc, html, Input, Output

engine = create_engine("postgresql+psycopg2://test:7246e@localhost/db_project")

schema_name = "shop"
conn = engine.connect().execution_options(
    schema_translate_map={None: schema_name})

df = None
with Session(engine) as session:
    query = session.query(
        CartGood.cart_goods_id,
        CartGood.shopping_cart_id,
        CartGood.good_id,
        Category.name.label('category_name'),
        Good.name.label('good_name'),
        CartGood.price_with_discount,
        CartGood.amount
    ).join(Good, CartGood.good_id == Good.good_id).join(Category, Good.category_id == Category.category_id).statement
    df = pd.read_sql(query, session.bind)
    df = df.groupby(["category_name", "good_name", "price_with_discount"]).agg({'amount': 'sum'}).reset_index()
    df.columns = ["Название категории", "Название товара", "Цена с скидкой", "Кол-во"]

    
    query = session.query(
        User.account_name,
        User.bonus_credits,
        Order.total_price
    ).join(ShoppingCart, ShoppingCart.user_name == User.account_name).join(Order, Order.shopping_cart_id == ShoppingCart.shopping_cart_id).statement
    df1 = pd.read_sql(query, session.bind)
    df1.columns = ["Имя пользователя", "Кол-во бонусов", "Цена заказа"]

bigger = df[df["Цена с скидкой"] > 10000][["Цена с скидкой", "Кол-во"]].sum()
lesser = df[["Цена с скидкой", "Кол-во"]].sum() - bigger

summary = pd.Series([bigger["Цена с скидкой"], lesser["Цена с скидкой"]], index=[">10000", "<10000"])
categories = df.groupby("Название категории").agg({"Цена с скидкой" : "sum", "Кол-во" : "sum"}).reset_index()

fig1 = px.bar(data_frame=summary,
            labels={
                "value": "Итоговая сумма",
                "index": "Цена товаров",
            })

fig2 = px.pie(data_frame=categories, names="Название категории", values="Цена с скидкой", title="Сумма цен товаров")
fig2_1 = px.pie(data_frame=categories, names="Название категории", values="Кол-во", title="Кол-во товаров в корзинах")

fig3 = px.scatter(data_frame=df1[["Кол-во бонусов", "Цена заказа"]], x = "Цена заказа", y = "Кол-во бонусов")

app = Dash(__name__)

colors = {
    'background': 'white',
    'text': '#4B5ED7'
}

fig1.update_layout(
    font_color = colors['text']
)
fig2.update_layout(
    font_color = colors['text']
)
fig2_1.update_layout(
    font_color = colors['text']
)
fig3.update_layout(
    font_color = colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Дисклеймер: Все гипотезы высосаны из пальца, из-за того что данные сгенерированы',
            style={'textAlign': 'center', 'color': colors['text']}),
    
    html.H2(children="1-ая гипотеза - значительная часть дохода получена с дорогих товаров (стоящие >10000)", 
            style={'textAlign': 'center', 'color': colors['text']}),
    dcc.Graph(figure=fig1),
    html.H2(children="По гистограмме можно определённо сказать, что большую часть прибыли приносят дорогие товары, значит наша гипотеза верна", 
            style={'textAlign': 'center', 'color': colors['text'], 'padding-bottom' : "60px"}),
    
    html.H2(children="2-ая гипотеза - больше всего тратится денег на товары из категории Электроника", 
            style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(children=[
        dcc.Graph(figure=fig2, style={'display': 'inline-block'}),
        dcc.Graph(figure=fig2_1, style={'display': 'inline-block'})
    ], style={'display':'flex', 'flex-direction':'row', 'textAlign': 'center'}),
    html.H2(children="По двум круговым диаграммам можно сказать такие вещи, кол-во товаров из разных категорий отличается не особо сильно, но всё равно наибольший доход приносит категория Электроника. Гипотеза верна", 
            style={'textAlign': 'center', 'color': colors['text'], 'padding-right' : "25%", 'padding-left' : "25%", 'padding-bottom' : "60px"}),
    
    html.H2(children="3-ая гипотеза - пользователи с большим кол-вом бонусов имеют более дорогие заказы", 
            style={'textAlign': 'center', 'color': colors['text']}),
    dcc.Graph(figure=fig3),
    html.H2(children="Данных кот наплакал конечно, но точно можно сказать, что никакой зависимости не прослеживается. Гипотеза неверна", 
            style={'textAlign': 'center', 'color': colors['text'], 'padding-right' : "25%", 'padding-left' : "25%", 'padding-bottom' : "60px"}),
])

app.run(debug=False)