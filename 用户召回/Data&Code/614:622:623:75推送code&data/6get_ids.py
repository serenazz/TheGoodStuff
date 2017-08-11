import pandas as pd
from pandas import HDFStore
import datetime
import csv


store=HDFStore('storage1.h5')
history=store['622pushed']
history=history["id"].tolist()

df=pd.read_csv("6.23_sleep.csv")
print(df.shape[0])
#剔除已推过
def if_in(row,list):
    if row["id"] in list:
        return 0
    else:
        return 1

df["if_keep"]= df.apply(lambda row: if_in(row,history), axis=1)
df=df.loc[df["if_keep"]==1]
print(df["if_keep"].value_counts())
df=df.drop("if_keep",1)


df=df.fillna(0)
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index) - df['last']).astype('timedelta64[D]').astype('int')
df["promotion_cnt"]=df["promotion_cnt"].astype(int)
df["num"]=df["num"].astype(int)
df["coupon_cnt"]=df["coupon_cnt"].astype(int)

df["if_new"]= df['first_order_interval'] == df['last_order_interval']
df["recently_joined"]=df["first_order_interval"]<=90
df["ratio"]=df.promotion_cnt/df.num
df["c_ratio"]=df.coupon_cnt/df.num
df["if_one_day"]= df['first_order_interval'] == df['last_order_interval']
def check_price_sen(row):
    if (row["ratio"]>0.5) or (row["c_ratio"]>0.5):
        return True
    else:
        return False
df["price_sen"]= df.apply(lambda row: check_price_sen(row), axis=1)
pushed_list=[]
'''
with open("6.22_guanzhu.csv",'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        pushed_list.append(row)
pushed_list=pushed_list[0]
for i in range(len(pushed_list)):
    pushed_list[i]=int(pushed_list[i])


#创建推送成功df
df["if_keep"]= df.apply(lambda row: if_in(row,pushed_list), axis=1)
df=df.loc[df["if_keep"]==0]
print(df["if_keep"].value_counts())
df_pushed=df.drop("if_keep",1)
#store.put('622pushed',df_pushed,format="table")
print(df_pushed.head(5))
store.close()

#df_push=df.loc[(df["price_sen"]==False)]
'''
df_push=df.sample(frac=0.5).reset_index(drop=True)
print(df_push.shape[0])
'''
with open("6.23push.csv",'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(df_push["id"].tolist())
print(df_push.head())
'''