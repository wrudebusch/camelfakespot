CREATE OR REPLACE VIEW popular_and_topdrop AS (
SELECT DISTINCT td.product_id, 
td.curret_price AS current_price, 
list_price, 
avg_price, 
td.previous_price, 
fs_grade, 
LTRIM(LTRIM(LTRIM(td.product_title, '"'),''''),'Price history for ') AS product_info, 
'https://www.amazon.com/dp/'||td.product_id AS url 
FROM topdrops AS td
JOIN popular as pop ON pop.product_id = td.product_id
JOIN fakespot_results AS fs ON td.product_id = fs.product_id)