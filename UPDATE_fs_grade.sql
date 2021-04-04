UPDATE graded_products AS g
SET fs_grade = f.fs_grade
FROM fakespot_results AS f
WHERE f.product_id = g.product_id;

TRUNCATE fakespot_results;


--SELECT * FROM graded_products WHERE fs_grade IS NOT NULL;