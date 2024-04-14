--Query 1
SELECT *
FROM authors
ORDER BY date_of_birth
LIMIT 10;

--Query 2
SELECT sale_items.item_price * sale_items.quantity AS sales_total
FROM sale_items
JOIN books ON sale_items.book_id = books.book_id
JOIN authors ON books.author_id = authors.id
WHERE authors.name ILIKE 'Lorelai Gilmore';

--Query 3
SELECT authors.name AS author, SUM(sale_items.item_price * sale_items.quantity) AS total_sales
FROM sale_items
JOIN books ON sale_items.book_id = books.id
JOIN authors ON books.author_id = authors.id
GROUP BY authors.name
ORDER BY total_sales DESC
LIMIT 10;

