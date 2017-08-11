import pandas as pd
from pandas import HDFStore
import datetime
import csv
history=[]
with open("pushed.csv") as f:
    R= csv.reader(f)
    for row in R:
        history.append(row)
df=pd.read_csv("lost_users.csv")
print(df.shape[0])
#剔除已推过
def if_in(row,list):
    if str(row["id"]) in list:
        return 0
    else:
        return 1

df["if_keep"]= df.apply(lambda row: if_in(row,history[0]), axis=1)
df=df.loc[df["if_keep"]==1]
print(df["if_keep"].value_counts())
df=df.drop("if_keep",1)

print(df.shape[0])

df=df.fillna(0)
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index) - df['last']).astype('timedelta64[D]').astype('int')
#df["promotion_cnt"]=df["promotion_cnt"].astype(int)
#df["num"]=df["num"].astype(int)
#df["coupon_cnt"]=df["coupon_cnt"].astype(int)
#df["recently_joined"]=df["first_order_interval"]<=90
#df["ratio"]=df.promotion_cnt/df.num
#df["c_ratio"]=df.coupon_cnt/df.num
#df["if_one_day"]= df['first_order_interval'] == df['last_order_interval']
def check_price_sen(row):
    if (row["ratio"]>0.5) or (row["c_ratio"]>0.5):
        return True
    else:
        return False
#df["price_sen"]= df.apply(lambda row: check_price_sen(row), axis=1)
df=df.loc[(df["last_order_interval"]<=90)&(df["last_order_interval"]>30)]
print(df.shape[0])
#df["id"].to_frame().to_csv("comparison_gourp",sep=',',index=False, line_terminator=',')

