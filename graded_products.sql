DROP VIEW graded_products;
CREATE OR REPLACE VIEW graded_products AS (
SELECT current_price AS current_price, fs_grade, LTRIM(LTRIM(LTRIM(product_title, '"'),''''),'Price history for ') AS product_info, 
	'https://www.amazon.com/dp/'||product_id AS url 
FROM (SELECT DISTINCT current_price, previous_price, topdrops.product_id, product_title, fs_grade, 'topdrops' as camel_source
FROM topdrops 
JOIN fakespot_results ON topdrops.product_id = fakespot_results.product_id
UNION
SELECT DISTINCT current_price, NULL AS previous_price, popular.product_id, product_title, fs_grade, 'popular' as camel_source
FROM popular
JOIN fakespot_results ON popular.product_id = fakespot_results.product_id) AS x
ORDER BY product_id)