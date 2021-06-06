CREATE OR REPLACE VIEW popular_and_topdrop AS (
SELECT DISTINCT td.product_id, 
td.current_price, 
list_price, 
avg_price, 
td.previous_price, 
fs_grade, 
LTRIM(TRIM(TRIM(td.product_title, '"'),''''),'Price history for ') AS product_info, 
'https://www.amazon.com/dp/'||td.product_id AS url,
pop.timestamp AS popular_ts,
td.timestamp AS topdrop_ts
FROM topdrops AS td
JOIN popular as pop ON pop.product_id = td.product_id
JOIN fakespot_results AS fs ON td.product_id = fs.product_id)