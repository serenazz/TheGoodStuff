SELECT `user`.`userid`, FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') AS 'shoudan',
c.last_order as "last_order", c.num_of_order, d.id, d.total_cnt, d.promotion_cnt, d.promotion_amt, d.regular_cnt,d.regular_amt from user
LEFT JOIN shoudanb ON `user`.`userid` = shoudanb.buyerid
LEFT JOIN (SELECT count(*) as num_of_order, payorder.buyerid, max(payorder.orderday) as last_order from payorder where payorder.orderstatus in (2,5)
GROUP BY payorder.buyerid) c on c.buyerid = `user`.`userid`
left join (SELECT
    paysuborder.userid as id,
    COUNT(*) AS total_cnt,
    a.cnt AS promotion_cnt,
    a.amt AS promotion_amt,
    b.cnt AS regular_cnt,
    b.amt AS regular_amt
FROM
    paysuborder
LEFT JOIN
    (
    SELECT k.id AS userid,
        COUNT(*) AS cnt,
        SUM(k.fee) / 100 AS amt
    FROM
        (
        SELECT
            SUM(paysuborder.promotionfee) AS fee,
            paysuborder.userid AS id
        FROM
            paysuborder
        where paysuborder.orderstatus in (2,5)
        GROUP BY
            paysuborder.orderid
    ) k
WHERE k.fee > 0
GROUP BY
    k.id
) a
ON
    paysuborder.userid = a.userid
LEFT JOIN
    (
    SELECT
        paysuborder.userid AS id,
        COUNT(*) AS cnt,
        SUM(paysuborder.price) / 100 AS amt
    FROM
        paysuborder
    WHERE
        paysuborder.promotionfee = 0
    GROUP BY
        paysuborder.userid
) b
ON
    paysuborder.userid = b.id
GROUP BY
    paysuborder.userid
ORDER BY
    a.cnt
DESC) d on d.id = user.userid
where c.last_order is not null and FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') is not null
and user.leaderid!=0
and c.last_order >="2017-03-14" and c.last_order <="2017-05-14"