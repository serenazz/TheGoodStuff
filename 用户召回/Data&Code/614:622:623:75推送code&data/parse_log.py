# coding: utf-8
import pandas as pd
from datetime import datetime
import csv
from pandas import HDFStore
urldic={
    'grouponCreate': '创建拼团',
    'grouponUpdate': '修改拼团',
    'grouponStatus': '邀请参团',
    'grouponMerch': '我要参团',
    'grouponBuy': '支付',
    'grouponOrders': '我的订单',
    'groupLeaderApply': '甄选师申请',
    'groupLeaderProfile': '完善资料',
    'groupLeaderResult': '提交成功',
    'groupLeaderSearch': '我的甄选搜索',
    'buyGroupMovie': '选择座位',
    'mine': '我的',
    'mineOrder': '我的订单',
    'orderDetail': '我的订单详情',
    'expressDetail': '物流详情',
    'myshare': '我的分享',
    'mineWallet': '我的收益',
    'mineWalletOrder': '甄选详情',
    'mineKefu': '联系客服',
    'minePage': '寻味师主页',
    'mineTransactionDetail': '交易明细',
    'mineTransactionDetailContent': '返利明细',
    'createStory': '添加产地故事',
    'storyVideo': '达人视频',
    'mineAddrs': '收货地址',
    'createAddr': '添加地址',
    'updateAddr': '修改地址',
    'mineCoupons': '优惠券',
    'receiveCoupon': '抢优惠券',
    'mineTeam': '我的团队',
    'mineTeamMember': '团队成员',
    'mineTeamRule': '组团规则',
    'mineFans': '我的会员',
    'mineSearchFans': '会员查询',
    'groupLeader': '我的好东西',
    'groupLeaderEdit': '编辑资料',
    'groupLeaderOrderStats': '当日统计',
    'groupLeaderOrderStatusMore': '更多订单',
    'afterSaleCreate': '申请售后',
    'afterSaleShow': '售后处理',
    'receivePackageCoupon': '抢优惠劵',
    'grouponText': '甄选文本',
    'mineLevel': '我的等级',
    'groupLeaderShareCoupon': '分享劵',
    'couponList': '奖励',
    'couponFinishList': '发完的优惠劵',
    'buyMovie': '确认订单',
    'mineTrainerTeam': '培训师团队',
    'mineTrainerTeamMember': '培训师团队',
    'trainerIncome': '我的收益',
    'inviteGroupLeaderList': '我邀请的小伙伴',
    'inviteGroupLeader': '培训师推荐收益',
    'trainerHistory': '培训师历史收益',
    'trainerMonthDetail': '培训师月结推荐收益详情',
    'mineAdviser': '我的甄选顾问',
    'discountMore': '特卖专场',
    'mineTeamMemberOrderStats': '团队成员',
    'groupLeaderRecommend': '我的好东西',
    'mineGuide': '新手教学',
    'mineIncome': '我的收益',
    'mineIncomeStats': '甄选收益',
    'mineIncomeStatsByMerch': '甄选收益',
    'mineIncomeStatsByMonth': '甄选收益',
    'mineIncomeStatsByMerchOrder': '甄选收益',
    'noOrders': '没有订单',
    'index': '首页',
    'merch': '商品详情',
    'buy': '确认订单',
    'rule': '分享规则',
    'orders': '我的订单',
    'evaluate': '晒单内容',
    'orderCreateEvaluate': '创建晒单',
    'movie': '选择座位',
    'explore': '首页',
    'exploreSearch': '首页搜索',
    'recommendMore': '我的甄选查看更多',
    'discover': '发现好东西',
    'pay': '支付',
    'paySuccess': '支付成功',
}
df=pd.DataFrame(columns=("time","userid","url","suburl"))
'''
with open("6.22push.csv") as f:
    reader=csv.reader(f)
    list_of_pushed=list(reader)[0]
'''

def read_log_file(log_file):
    for line in open(log_file):
        try:
            data=line.split(" ")
            day = data[0].strip("[")
            time=data[1].strip("]")
            time= day+" "+time
            time = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
            userid=int(data[2])
            url = data[3].strip("\n")

            if (time>datetime.strptime(day+" "+"18:25:00",'%Y-%m-%d %H:%M:%S')): #and (str(userid) in list_of_pushed):
                url= url.split("/share/")[1]
                try:
                    url= url.split("?")
                    suburl=url[1]
                    try:
                        url=urldic[url[0]]
                    except:
                        url=url[0]
                except Exception:
                    try:
                        url=urldic[url[0]]
                    except:
                        url= url
                    suburl=0
                df.loc[len(df)]=[time,userid,url,suburl]

        except Exception:
            print(":", Exception)
            print(line)

read_log_file('614route.log')
df["userid"]=df["userid"].astype(int)
df["suburl"]=df["suburl"].astype(str)
store=HDFStore('storage1.h5')
store.put('614_617all_browse',df,format="table")



