用户最喜欢购买时间分布（未减权）
SELECT
    d.time,
    COUNT(d.id) FROM(SELECT c.id, c.time
    FROM(SELECT a.id AS id, MAX(cnt) as m
        FROM(SELECT payorder.buyerid id, FROM_UNIXTIME(payorder.dateline, "%H") AS Hour, FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d %H") AS TIME,
                COUNT(*) AS cnt
            FROM payorder
            left join paysuborder on payorder.orderid=paysuborder.orderid
                where FROM_UNIXTIME(payorder.dateline, "%Y-%m") > "2017-03"
                and paysuborder.promotionfee=0
            GROUP BY
                payorder.buyerid,
                FROM_UNIXTIME(payorder.dateline, "%H")) AS a
            group by a.id) b
	INNER JOIN( SELECT
                payorder.buyerid id,
                FROM_UNIXTIME(payorder.dateline, "%H") AS TIME,
                COUNT(*) AS cnt
            FROM payorder
            left join paysuborder on payorder.orderid=paysuborder.orderid
                where FROM_UNIXTIME(payorder.dateline, "%Y-%m") >= "2017-03"
                and paysuborder.promotionfee=0
            GROUP BY payorder.buyerid, FROM_UNIXTIME(payorder.dateline, "%H"))  AS c 
ON c.id = b.id AND c.cnt = b.m) d
GROUP BY d.time

每级甄选师数和会员数
select a.rank, count(*), count(distinct a.leader),count(*)/count(distinct a.leader) from (
    select user.userid,user.leaderid leader, saler.rank rank from user left join saler on user.leaderid = saler.userid)a group by a.rank


甄选师分类
SELECT saler.statustag,
       category.title,
       COUNT(saler.userid)
FROM saler,
     category
WHERE saler.status = 1
  AND saler.statustag = category.categoryid
GROUP BY saler.statustag


=================================================================================
参团还是不参团 （grouponid：从寻味师页面购买。这个也可能和recommenderid不一样）

SELECT e.time,
       e.num AS '总单量',
       concat(a.num, ' ', round(a.num*100/e.num, 2), '%') AS '参团分销',
       b.num AS '非参团分销',
       concat(round(b.num*100/e.num, 2), '%') AS '占比',
       concat(c.num, ' ', round(c.num*100/e.num, 2), '%') AS '关闭团长订单',
       concat(d.num, ' ', round(d.num*100/e.num, 2), '%') AS '纯零售'
  FROM(
SELECT FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d') AS time, COUNT(*) AS num
  FROM `payorder`
 WHERE `payorder`.`orderstatus` IN(2, 5)
 GROUP BY FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d')) AS e
  LEFT JOIN(
SELECT FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d') AS time, COUNT(*) AS num
  FROM `payorder`
 WHERE `payorder`.`orderstatus` IN(2, 5)
   AND `payorder`.`grouponid`!= 0
   AND `payorder`.`recommenduserid`!= 0
 GROUP BY FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d')) AS a ON e.time= a.time
  LEFT JOIN(
SELECT FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d') AS time, COUNT(*) AS num
  FROM `payorder`
 WHERE `payorder`.`orderstatus` IN(2, 5)
   AND `payorder`.`grouponid`= 0
   AND `payorder`.`recommenduserid`!= 0
 GROUP BY FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d')) AS b ON e.time= b.time
  LEFT JOIN(
SELECT FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d') AS time, COUNT(*) AS num
  FROM `payorder`
 WHERE `payorder`.`orderstatus` IN(2, 5)
   AND `payorder`.`grouponid`!= 0
   AND `payorder`.`recommenduserid`= 0
 GROUP BY FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d')) AS c ON e.time= c.time
  LEFT JOIN(
SELECT FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d') AS time, COUNT(*) AS num
  FROM `payorder`
 WHERE `payorder`.`orderstatus` IN(2, 5)
   AND `payorder`.`grouponid`= 0
   AND `payorder`.`recommenduserid`= 0
 GROUP BY FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d')) AS d ON e.time= d.time
 ORDER BY e.time DESC


================================================================================================

单量
select payorder.buyerid, count(*) from payorder where payorder.orderstatus in (2,5) and payorder.orderday>="2016-04-01" group by payorder.buyerid order by count(*) desc

＃甄选师流水，箱数
 SELECT saler.rank, SUM((`paysuborder`.`price` - paysuborder.promotionfee) * `paysuborder`.`quantity`+ `paysuborder`.`expressfee` - `paysuborder`.`couponmoney`) /100 AS '流水', SUM(`paysuborder`.`quantity`) AS '箱数'
  FROM `paysuborder`, `payorder` 
    LEFT JOIN `saler` AS saler ON `payorder`.`recommenduserid`= saler.`userid`
 WHERE `paysuborder`.`orderid`= `payorder`.`orderid`
 AND `paysuborder`.`orderstatus` IN(2, 5)
 AND FROM_UNIXTIME(`payorder`.`dateline`, '%Y-%m-%d %H:%i:%s')>= '2016-10-01 00:00:00'
 GROUP BY saler.rank
 ORDER BY `箱数` DESC

＃用户最后一次购买商品
SELECT a.buyerid, from_unixtime(a.dateline, "%Y-%m-%d"), c.name FROM `payorder` a 
LEFT JOIN `payorder` b ON a.buyerid = b.buyerid AND a.dateline < b.dateline 
LEFT JOIN( select merchandise.abbreviation name, merchandise.merchandiseid from merchandise) c 
on c.merchandiseid = a.merchandiseid WHERE b.dateline is NULL and a.buyerid in (195070)
==================================================================================================
＃算用户参活动频率
SELECT
    paysuborder.userid,
    COUNT(*) AS total_cnt,
    a.cnt AS promotion_cnt,
    a.amt AS promotion_amt,
    b.cnt AS regular_cnt,
    b.amt AS regular_amt
FROM
    paysuborder
LEFT JOIN
    (
    SELECT c.id AS userid,
        COUNT(*) AS cnt,
        SUM(c.fee) / 100 AS amt
    FROM
        (
        SELECT
            SUM(paysuborder.promotionfee) AS fee,
            paysuborder.userid AS id
        FROM
            paysuborder
        GROUP BY
            paysuborder.orderid
    ) c
WHERE c.fee > 0
GROUP BY
    c.id
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
WHERE
    a.cnt IS NOT NULL
GROUP BY
    paysuborder.userid
ORDER BY
    a.cnt
DESC
    


=================================================================================
＃调用户首末单，单量和用户的优惠券数量
SELECT
    `user`.`userid`,
    FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') AS 'shoudan',
    c.last_order AS "last_order",
    c.num_of_order,
    d.total_cnt,
    d.promotion_cnt,
    coupon.coupon_cnt
FROM
    USER
LEFT JOIN
    shoudanb
ON
    `user`.`userid` = shoudanb.buyerid
LEFT JOIN
    (
    SELECT
        payorder.buyerid,
        COUNT(*) AS coupon_cnt
    FROM
        payorder
    WHERE
        payorder.couponmoney > 0
        and payorder.orderstatus in (2,5)
        group by payorder.buyerid) as coupon
    ON
        coupon.buyerid = `user`.`userid`
LEFT JOIN
            (
                SELECT
                COUNT(*) AS num_of_order,
                payorder.buyerid,
                MAX(payorder.orderday) AS last_order
                FROM
                payorder
                WHERE
                payorder.orderstatus IN(2, 5)
                GROUP BY
                payorder.buyerid
            ) c
    ON
        c.buyerid = `user`.`userid`
LEFT JOIN
    (
    SELECT
        paysuborder.userid AS id,
        COUNT(*) AS total_cnt,
        a.cnt AS promotion_cnt,
        a.amt AS promotion_amt,
        b.cnt AS regular_cnt,
        b.amt AS regular_amt
    FROM
        paysuborder
    LEFT JOIN
        (
        SELECT
            k.id AS userid,
            COUNT(*) AS cnt,
            SUM(k.fee) / 100 AS amt
        FROM
            (
            SELECT
                SUM(paysuborder.promotionfee) AS fee,
                paysuborder.userid AS id
            FROM
                paysuborder
            WHERE
                paysuborder.orderstatus IN(2, 5)
            GROUP BY
                paysuborder.orderid
        ) k
    WHERE
        k.fee > 0
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
where paysuborder.orderstatus in (2,5)
GROUP BY
    paysuborder.userid
ORDER BY
    a.cnt
DESC
) d
ON
    d.id = USER.userid
WHERE
    c.last_order IS NOT NULL AND FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') IS NOT NULL 
    and c.last_order >="2017-05-22" and c.last_order <="2017-06-07"
    and user.nocallbackwxmsg!=1
    and user.leaderid!=0

=-===================================================================
＃用户的下单时间／小时
SELECT
    payorder.buyerid id,
    DAYOFWEEK(
        FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d %H")
    ) AS DAY,
    FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d %H") AS TIME
FROM
    payorder
LEFT JOIN
    paysuborder
ON
    payorder.orderid = paysuborder.orderid
WHERE
paysuborder.promotionfee = 0 AND DAYOFWEEK(
        FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d %H")
    ) IN(2, 3, 4, 5, 6)
    and FROM_UNIXTIME(payorder.dateline, "%Y-%m") > "2017-03"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m") < "2017-06"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") != "2017-04-19"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-04-20"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-04-21"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-04-22"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-04-23"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-12"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-13"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-14"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-25"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-26"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-27"
                and FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d") !="2017-05-28"

==============================================================================================
＃甄选师分类
SELECT workingsaler.userid,
       danliangweidu.danliang,
       zuijindanweidu.zuijin
FROM
  (SELECT saler.userid
   FROM saler
   WHERE saler.statustag IN(190,
                            191,
                            192,
                            193)) AS workingsaler
LEFT JOIN
  (SELECT a.salerid,
          SUM(a.danliang) AS danliang
   FROM
     (SELECT `user`.`userid`,
             saler.userid AS salerid,
             COUNT(payorder.orderid) AS danliang
      FROM saler,
           `user`,
           payorder
      WHERE saler.status = 1
        AND `user`.`leaderid` = `saler`.`userid`
        AND payorder.buyerid = `user`.`userid`
        AND payorder.orderstatus IN (2,
                                     5)
        AND payorder.orderday >= '2017-04-25'
      GROUP BY `user`.`userid`) AS a
   GROUP BY a.salerid) AS danliangweidu ON workingsaler.userid = danliangweidu.salerid
LEFT JOIN
  (SELECT a.salerid,
          datediff(curdate(),MAX(a.zuijin)) AS zuijin
   FROM
     (SELECT `user`.`userid`,
             saler.userid AS salerid,
             MAX(payorder.orderday) AS zuijin
      FROM saler,
           `user`,
           payorder
      WHERE saler.status = 1
        AND `user`.`leaderid` = `saler`.`userid`
        AND payorder.buyerid = `user`.`userid`
        AND payorder.orderstatus IN (2,
                                     5)
      GROUP BY `user`.`userid`) AS a
   GROUP BY a.salerid) AS zuijindanweidu ON workingsaler.userid = zuijindanweidu.salerid

计算不同标签的甄选师数和会员数
select a.tag, a.title, count(*), count(distinct a.leader) from (SELECT saler.statustag tag, category.title title, saler.userid leader FROM saler, category WHERE saler.status = 1 AND saler.statustag = category.categoryid)a right join user on user.leaderid=a.leader group by a.tag
多少购买过会员没有甄选师
select count(distinct payorder.buyerid), count(*), sum(payorder.amount) from payorder
left join user on user.userid=payorder.buyerid 
where user.leaderid=0  and payorder.orderday>="2017-03-01"
==========================================================
甄选师流水。拉辛等
SELECT
    a.id,
    a.cnt,
    a.amt,
    a.boxes
    c.new_cnt
FROM
    (
    SELECT
        T(*) ASpayorder.recommenduserid AS id COUN cnt,
        SUM(
            (
                `paysuborder`.`price` - paysuborder.promotionfee
            ) * `paysuborder`.`quantity` + `paysuborder`.`expressfee` - `paysuborder`.`couponmoney`
        ) / 100 AS amt,
        SUM(`paysuborder`.`quantity`) AS boxes
    FROM
        `paysuborder`,
        `payorder`
    WHERE
        `paysuborder`.`orderid` = `payorder`.`orderid` AND paysuborder.orderstatus IN(2, 5) AND payorder.orderday >= "2017-05-01" AND payorder.orderday <= "2017-05-31"
    GROUP BY
        payorder.recommenduserid
) a
LEFT JOIN
    (
    SELECT
        b.pid AS id,
        COUNT(*) AS new_cnt
    FROM
        (
        SELECT
            saler.userid,
            saler.pid AS pid
        FROM
            saler
        WHERE
            FROM_UNIXTIME(saler.dateline "%Y-%m-%d") >= "2017-05-01" AND FROM_UNIXTIME(saler.dateline "%Y-%m-%d") <= "2017-05-31"
    ) b
GROUP BY
    b.pid) c
ON
    c.id = a.id



=================
多少流失用户

select count(*) from user
LEFT JOIN
            (
                SELECT
                COUNT(*) AS num_of_order,
                payorder.buyerid,
                MAX(payorder.orderday) AS last_order
                FROM
                payorder
                WHERE
                payorder.orderstatus IN(2, 5)
                GROUP BY
                payorder.buyerid
            ) c
    ON
        c.buyerid = `user`.`userid`
        where c.last_order <"2017-3-22"
=======
只购买过1次的用户
select count(*) from ( select payorder.buyerid,count(*) as cnt from 
  payorder where payorder.orderstatus in (2,5) group by payorder.buyerid) a where a.cnt=1
=============
买过一次的用户的甄选师情况
select count(*) from (select b.buyerid, saler.statustag from
    (
    SELECT
        a.buyerid,user.leaderid from 
        (
        SELECT
            payorder.buyerid,
            COUNT(*) AS cnt
        FROM
            payorder
        WHERE
            payorder.orderstatus IN(2, 5)
        GROUP BY
            payorder.buyerid
    ) a
left join user on user.userid=a.buyerid
WHERE
    a.cnt = 1)b
    
left join saler on saler.userid=b.leaderid) c where c.statustag=

===========================
观望用户
select count(*) from (select * from userweixin left join 
    (select payorder.buyerid, count(*) as c from payorder group by payorder.buyerid ) a on a.buyerid=userweixin.userid where userweixin.subscribed=1)b where b.c is not null

==============================
#六月份首单，6-8月订单，是否用券, 是否甄选师，首单品
SELECT
    shoudanb.buyerid,
    FROM_UNIXTIME(shoudanb.dateline, "%Y-%m-%d"),
    b.if_zxs,
    a.orderday,
    a.coupon as if_normal_c,
    c.name as first_name,
    a.abb as normal_name,
    c.couponc as if_first_c
FROM
    shoudanb
left join(
    select payorder.orderid, 
    payorder.merchandiseid,
    merchandise.abbreviation as name, 
    case when(payorder.couponmoney>0) then 1 else 0 end as couponc
    from payorder, merchandise 
    where merchandise.merchandiseid=payorder.merchandiseid)c on c.orderid=shoudanb.orderid
LEFT JOIN
    (
    SELECT
        payorder.buyerid,
        payorder.orderday,
        payorder.merchandiseid,
        merchandise.abbreviation as abb,
        case when(payorder.couponmoney>0) then 1 else 0 end as coupon
    FROM
        payorder
    left join merchandise on payorder.merchandiseid=merchandise.merchandiseid
    left join shoudanb on shoudanb.buyerid=payorder.buyerid
    WHERE
        FROM_UNIXTIME(payorder.dateline, "%Y-%m-%d")>=FROM_UNIXTIME(shoudanb.dateline, "%Y-%m-%d") AND payorder.orderstatus IN(2, 5) and FROM_UNIXTIME(payorder.dateline,"%Y-%m")<"2017-9" 
        and payorder.orderid!=shoudanb.orderid) a
    on a.buyerid=shoudanb.buyerid
left join
    (select user.userid,case when(user.userid=user.leaderid) then 1 else 0 end as if_zxs from user)b on b.userid=shoudanb.buyerid
WHERE
    FROM_UNIXTIME(shoudanb.dateline, "%Y-%m")="2017-06"
==============================
零售用户 --2017-4052;4455
select count(*) from (
SELECT
    payorder.buyerid AS userid,
    SUM(payorder.recommenduserid) AS tuan,
    COUNT(payorder.orderid) AS orders
FROM
    payorder
WHERE
    payorder.orderstatus IN(2, 5) AND payorder.orderday >= '2017-01-01'
GROUP BY
    payorder.buyerid)a
where a.tuan=0
====================
7.5召回
限定：不给

SELECT
    `user`.`userid`,
    FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') AS 'shoudan',
    c.last_order AS "last_order",
    c.num_of_order,
    user.leaderid,
    saler.statustag
FROM
    user
LEFT JOIN
    shoudanb
ON
    `user`.`userid` = shoudanb.buyerid
LEFT JOIN
            (
                SELECT
                COUNT(*) AS num_of_order,
                payorder.buyerid,
                MAX(payorder.orderday) AS last_order
                FROM
                payorder
                WHERE
                payorder.orderstatus IN(2, 5)
                GROUP BY
                payorder.buyerid
            ) c
    ON
        c.buyerid = user.userid
left join saler on saler.userid=user.leaderid
WHERE
    c.last_order IS NOT NULL AND FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') IS NOT NULL 
    and c.last_order >="2017-04-06" and c.last_order <"2017-06-06"
    and user.nocallbackwxmsg!=1
    and user.leaderid!=0
    and user.leaderid!=user.userid
    and saler.statustag in (193,192,190,191)

==========================
76重流失多单
SELECT
    `user`.`userid`,
    FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') AS 'shoudan',
    c.last_order AS "last_order",
    c.num_of_order,
    user.leaderid,
    saler.statustag
FROM
    user
LEFT JOIN
    shoudanb
ON
    `user`.`userid` = shoudanb.buyerid
LEFT JOIN
            (
                SELECT
                COUNT(*) AS num_of_order,
                payorder.buyerid,
                MAX(payorder.orderday) AS last_order
                FROM
                payorder
                WHERE
                payorder.orderstatus IN(2, 5)
                GROUP BY
                payorder.buyerid
            ) c
    ON
        c.buyerid = user.userid
left join saler on saler.userid=user.leaderid
WHERE
    c.last_order IS NOT NULL AND FROM_UNIXTIME(shoudanb.dateline, '%Y-%m-%d') IS NOT NULL 
    and c.last_order <"2017-04-06"
    and user.nocallbackwxmsg!=1
    and user.leaderid!=0
    and user.leaderid!=user.userid
    and saler.statustag in (193,192,190,191)
189
流失
188
新手活跃
193
挽留
192
发展
194
新手低迷
190
核心
195
新手不满7天
191
保持
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
查询活动开始12小时没有领券的人
select user.userid from
user
LEFT JOIN
    saler
ON
    USER.leaderid = saler.userid
LEFT JOIN
    userweixin
ON
    userweixin.userid = USER.userid
where user.userid not in 
(
    SELECT
    `yhdx-coupon`.usercoupon.userid
FROM
    `yhdx-coupon`.usercoupon
WHERE
FROM_UNIXTIME(
        `yhdx-coupon`.usercoupon.dateline,
        "%Y-%m-%d %H-%i-%s"
    ) < "2017-07-17 12:00:00" and `yhdx-coupon`.usercoupon.couponid in (3759,
3758,
3757,
3756,
3752，
3751
3750))
and 
userweixin.subscribed = 1 AND USER.leaderid != 0 AND saler.statustag IN(193, 192, 190, 191)
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
看购物车里加的品类
SELECT a.abbreviation,count(*) FROM `cart` 
left join (select merchandise.abbreviation,merchtype.merchtypeid from merchandise,merchtype 
    where merchtype.merchandiseid=merchandise.merchandiseid)a 
on a.merchtypeid=cart.merchtypeid group by a.abbreviation order by count(*) DESC

============================
总订单
SELECT
    COUNT(DISTINCT payorder.orderid)
FROM
    payorder
LEFT JOIN
    USER
ON
    payorder.buyerid = USER.userid
LEFT JOIN paysuborder on 
    paysuborder.orderid = payorder.orderid
WHERE
    payorder.orderday >"2017-07-11" AND USER.leaderid != 0
购物车订单
SELECT
    COUNT(*)
FROM
    (
    SELECT
        payorder.orderid
    FROM
        payorder
    LEFT JOIN
        paysuborder
    ON
        paysuborder.orderid = payorder.orderid
    WHERE
        payorder.orderday > "2017-07-11"
    GROUP BY
        paysuborder.orderid
    HAVING
        COUNT(payorder.orderid) > 1
) a

    所有某日订单-后用Pythonfilter出购物车多商品
    SELECT
    *
FROM
    (
    SELECT
        payorder.orderid AS orderid,
        paysuborder.suborderid AS subid,
        paysuborder.merchandiseid
    FROM
        payorder
    LEFT JOIN
        paysuborder
    ON
        paysuborder.orderid = payorder.orderid
    WHERE
        payorder.orderday = "2017-07-17"
        AND payorder.orderstatus IN(2, 5)
    ORDER BY
        payorder.orderid
) a
================
717活动
select user.userid from
user
LEFT JOIN
    saler
ON
    USER.leaderid = saler.userid
LEFT JOIN
    userweixin
ON
    userweixin.userid = USER.userid
where user.userid not in
(
    SELECT
    `yhdx-coupon`.usercoupon.userid
FROM
    `yhdx-coupon`.usercoupon
WHERE
FROM_UNIXTIME(
        `yhdx-coupon`.usercoupon.dateline,
        "%Y-%m-%d %H-%i-%s"
    ) < "2017-07-17 13:00:00" and `yhdx-coupon`.usercoupon.couponid in (3759,
3758,
3757,
3756,
3752,
3751,
3750))
and
userweixin.subscribed = 1 AND USER.leaderid != 0 AND saler.statustag IN(193, 192, 190, 191)
AND recall!=1!!!!!


活动调没关注，末单三个域内手机号

select recipientaddress.tel from
user
LEFT JOIN
    saler
ON
    USER.leaderid = saler.userid
LEFT JOIN
    userweixin
ON
    userweixin.userid = USER.userid
left join modanb on modanb.buyerid=user.userid
left join recipientaddress on recipientaddress.userid=user.userid
where user.userid not in
(
    SELECT
    `yhdx-coupon`.usercoupon.userid
FROM
    `yhdx-coupon`.usercoupon
WHERE
FROM_UNIXTIME(
        `yhdx-coupon`.usercoupon.dateline,
        "%Y-%m-%d %H-%i-%s"
    ) < "2017-07-17 13:00:00" and `yhdx-coupon`.usercoupon.couponid in (3759,
3758,
3757,
3756,
3752,
3751,
3750))
and
userweixin.subscribed = 0 AND USER.leaderid != 0 AND saler.statustag IN(193, 192, 190, 191) and 
from_unixtime(modanb.dateline, "%Y-%m-%d")>"2017-04-17" 
and recipientaddress.isdefault=1
============
某天新单用户

select payorder.buyerid, merchandise.abbreviation,paysuborder.orderid,paysuborder.merchandiseid ,payorder.couponmoney from paysuborder left join 
payorder on payorder.orderid=paysuborder.orderid 
left join merchandise on merchandise.merchandiseid=paysuborder.merchandiseid
left join user on paysuborder.userid=user.userid
where payorder.isneworder = 1
and payorder.orderday="2017-07-21"
and payorder.orderstatus in (2,5)
and user.leaderid!=0
and user.userid!=user.leaderid








