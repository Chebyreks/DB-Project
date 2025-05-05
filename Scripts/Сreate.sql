DROP SCHEMA IF EXISTS shop CASCADE;
CREATE SCHEMA shop;
SET search_path TO shop;

CREATE TABLE users (
    account_name VARCHAR(30) PRIMARY KEY,
    email VARCHAR(200) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    bonus_credits INT DEFAULT 0
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE goods (
    good_id SERIAL PRIMARY KEY,
    category_id INT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
	name VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    amount_in_stock INT NOT NULL
);

CREATE TABLE shopping_carts (
    shopping_cart_id SERIAL PRIMARY KEY,
    user_name VARCHAR(30) NOT NULL REFERENCES users(account_name) ON DELETE CASCADE,
    active BOOL DEFAULT TRUE
);

CREATE TABLE cart_goods (
    cart_goods_id SERIAL PRIMARY KEY,
    shopping_cart_id INT NOT NULL REFERENCES shopping_carts(shopping_cart_id) ON DELETE CASCADE,
    good_id INT NOT NULL REFERENCES goods(good_id),
    price_with_discount INT NOT NULL,
    amount INT NOT NULL
);

CREATE TABLE delivery_vehicle (
    delivery_id SERIAL PRIMARY KEY,
    vehicle VARCHAR(30) NOT NULL,
    vacant BOOL DEFAULT TRUE,
    storage_adress VARCHAR(200)
);

CREATE TABLE delivery_agent (
    agent_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES delivery_vehicle(delivery_id) ON DELETE SET NULL,
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    active BOOL DEFAULT TRUE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    shopping_cart_id INT NOT NULL REFERENCES shopping_carts(shopping_cart_id),
    agent_id INT NOT NULL REFERENCES delivery_agent(agent_id),
    delivery_address VARCHAR(200) NOT NULL,
    total_price INT NOT NULL,
    spent_bonus_credits INT DEFAULT 0
);

CREATE TABLE delivery_vehicle_log (
    id SERIAL PRIMARY KEY,
    vehicle_id INT NOT NULL REFERENCES delivery_vehicle(delivery_id),
    agent_id INT NOT NULL REFERENCES delivery_agent(agent_id),
    time_start TIMESTAMP NOT NULL,
    time_stop TIMESTAMP
);



-- Представления:

-- Представление в котором содержатся товары не лежащие на складе, но числящиеся на сайте
CREATE OR REPLACE VIEW goods_not_in_stock AS SELECT * FROM goods
WHERE amount_in_stock = 0;

-- Представление в котором содержится информация о всех активных агентах использующие корпоративный транспорт
CREATE OR REPLACE VIEW available_delivery_agents AS
SELECT 
    da.agent_id,
    da.name || ' ' || da.surname AS agent_full_name,
    dv.delivery_id,
    dv.vehicle,
    dv.storage_adress
FROM 
    delivery_agent da
JOIN 
    delivery_vehicle dv ON da.vehicle_id = dv.delivery_id
WHERE 
    da.active = TRUE 
    AND dv.vacant = FALSE;



-- Индексы:

-- Создаём индексы для нахождения активных агентов (часто их нужно искать)
CREATE INDEX agent_active_index ON delivery_agent(active)
WHERE active = TRUE;

-- Создаём индексы для столбца id корзин (тоже часто придётся проходить)
CREATE INDEX goods_of_cart_index ON cart_goods(shopping_cart_id);



-- Функции и процедуры:

-- Функция для получения id наиболее подходящего агента доставки (просто у которого меньше всех заказов)
SET search_path TO shop;
CREATE OR REPLACE FUNCTION find_best_delivery_agent(order_id INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    res_agent_id INT;
BEGIN
    res_agent_id := (SELECT agent_id FROM orders GROUP BY agent_id ORDER BY count(*));
    RETURN res_agent_id;
END;
$$;

-- Процедура для добавления скидки к продукту (в случае какиех-то комбо)
CREATE OR REPLACE PROCEDURE apply_discount(discount_percent INT, i_cart_goods_id INT)
language plpgsql
AS $$
BEGIN
    UPDATE cart_goods
    SET price_with_discount = (price_with_discount * discount_percent) / 100
	WHERE cart_goods_id = i_cart_goods_id; 
END;
$$;

-- Процедура для вычета баллов при их использовании
CREATE OR REPLACE PROCEDURE apply_bonuses(bonuses_spent INT, i_order_id INT)
language plpgsql
AS $$
BEGIN
    UPDATE orders
    SET total_price = (total_price - bonuses_spent), spent_bonus_credits = bonuses_spent
	WHERE order_id = i_order_id; 
END;
$$;



-- Триггеры

-- Функция оформления заказа (высчитывания итоговой суммы заказа )
CREATE OR REPLACE FUNCTION calculate_total_price()
RETURNS TRIGGER AS $$
DECLARE
    total INT := 0;
BEGIN
    -- Обновляем цену с учетом бонусов (в данном случае бонусы не используем)
    NEW.total_price := (SELECT SUM(price_with_discount * amount) FROM cart_goods WHERE shopping_cart_id = NEW.shopping_cart_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер при создании заказа
CREATE OR REPLACE TRIGGER trg_calculate_total_price
BEFORE INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION calculate_total_price();

-- Функция проверки на то что товар есть на складе
SET search_path TO shop;
CREATE OR REPLACE FUNCTION check_good_amount()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    stock_amount INT := 0;
BEGIN
    SELECT amount_in_stock INTO stock_amount FROM goods WHERE good_id = NEW.good_id;
    IF stock_amount < NEW.amount THEN
        RAISE EXCEPTION 'Not enough goods in stock. Available: %', stock_amount;
    END IF;
    RETURN NEW;
END;
$$;

-- Триггер для проверки наличия на складе
CREATE OR REPLACE TRIGGER trg_check_good_amount
BEFORE INSERT ON cart_goods
FOR EACH ROW
EXECUTE FUNCTION check_good_amount();

-- Функция появления нового товара в корзине (на этом моменте могут пройти проверки на скидки)
CREATE OR REPLACE FUNCTION set_price_with_discount()
RETURNS TRIGGER AS $$
BEGIN
    -- Обновляем цену с учетом скидки (в данном случае всегда подставляя цену из таблицы goods)
    NEW.price_with_discount := (SELECT price FROM goods WHERE good_id = NEW.good_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер при создании товара из корзины
CREATE OR REPLACE TRIGGER trg_set_price_with_discount
BEFORE INSERT ON cart_goods
FOR EACH ROW
EXECUTE FUNCTION set_price_with_discount();
