CREATE TABLE graded_products AS 
SELECT DISTINCT p.curret_price
, p.list_price
, t.previous_price
, p.avg_price
, p.product_id
, p.product_title
, p.page_num
, p."timestamp"
, NULL AS fs_grade
	FROM public.popular AS p
	JOIN public.top_drops AS t ON t.product_id=p.product_id;