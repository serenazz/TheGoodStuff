查单量
SELECT
    COUNT(*)
FROM
    paysuborder
    left join payorder on 
 payorder.orderid = paysuborder.orderid where     paysuborder.orderstatus IN(2, 5) AND payorder.orderday = "2017-07-17"