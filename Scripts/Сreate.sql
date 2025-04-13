DROP SCHEMA IF EXISTS shop CASCADE;
CREATE SCHEMA shop;
SET search_path TO shop;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    account_name VARCHAR(30),
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
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
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
CREATE TRIGGER trg_calculate_total_price
BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION calculate_total_price();

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
CREATE TRIGGER trg_set_price_with_discount
BEFORE INSERT OR UPDATE ON cart_goods
FOR EACH ROW
EXECUTE FUNCTION set_price_with_discount();