SET search_path TO shop;

--1 Получить всех пользователей, у которых бонусные баллы больше 100.
SELECT * 
FROM users 
WHERE bonus_credits > 100;

--2 Id пяти самых дорогих товаров
SELECT good_id, price
FROM goods
ORDER BY price DESC
LIMIT 5;

--3 Получить кол-во товара в каждой категории
SELECT g.category_id, c.name, COUNT(*) AS goods_count
FROM goods g
LEFT JOIN categories c ON c.category_id = g.category_id
GROUP BY g.category_id, c.name;

--4 Суммарная стоимость товаров в каждой активной корзине.
SELECT sc.shopping_cart_id, SUM(cg.price_with_discount * cg.amount) AS total
FROM shopping_carts sc
LEFT JOIN cart_goods cg ON sc.shopping_cart_id = cg.shopping_cart_id
WHERE sc.active = true
GROUP BY sc.shopping_cart_id;

--5 Найти имя пользователя с наибольшим количеством бонусов.
SELECT user_id, account_name, bonus_credits
FROM users
WHERE bonus_credits = (SELECT MAX(bonus_credits) FROM users);

--6 Товары из корзин со стоимостью больше 100000
SELECT g.good_id, g.price
FROM goods g
WHERE g.good_id IN (
	SELECT cgg.good_id
	FROM cart_goods cgg
	WHERE cgg.shopping_cart_id IN (
	    SELECT cg.shopping_cart_id
	    FROM cart_goods cg
	    GROUP BY cg.shopping_cart_id
	    HAVING SUM(cg.price_with_discount * cg.amount) > 100000)
);

--7 Ранг товаров внутри одной категории
SELECT good_id, category_id, price,
       RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank
FROM goods;

--8 Ранг агентов по кол-ву заказов
SELECT agent_id, order_count,
       DENSE_RANK() OVER (ORDER BY order_count DESC) AS rank_by_orders
FROM (
    SELECT agent_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY agent_id
);

--9 Вывод длительности использования транспорта в минутах
SELECT agent_id,
       ROUND(EXTRACT(EPOCH FROM (time_stop - time_start) / 60), 2) AS duration
FROM delivery_vehicle_log
WHERE time_stop IS NOT NULL
ORDER BY duration;

--10 Выводит за каждый период использования, прошлого агента использова транспорт
SELECT vehicle_id, agent_id,
       time_start,
       LAG(agent_id) OVER (PARTITION BY vehicle_id ORDER BY time_start) AS previous_agent
FROM delivery_vehicle_log;

--11 Максимальные и минимальные цены за товары в каждой категории
SELECT 
    c.category_id,
    c.name AS category_name,
    max_g.good_id AS max_price_good_id,
    max_g.name AS max_price_good_name,
    max_g.price AS max_price,
    min_g.good_id AS min_price_good_id,
    min_g.name AS min_price_good_name,
    min_g.price AS min_price
FROM categories c

LEFT JOIN goods max_g 
  ON max_g.category_id = c.category_id
 AND max_g.price = (
     SELECT MAX(price)
     FROM goods g
     WHERE g.category_id = c.category_id
 )

LEFT JOIN goods min_g 
  ON min_g.category_id = c.category_id
 AND min_g.price = (
     SELECT MIN(price)
     FROM goods g
     WHERE g.category_id = c.category_id
 );

--12 Агенты которые ни разу не пользовались корпоративным транспортом
SELECT a.agent_id, a.name, a.surname
FROM delivery_agent a
WHERE NOT EXISTS (
    SELECT 1
    FROM delivery_vehicle_log l
    WHERE l.agent_id = a.agent_id
);