from  pandas import HDFStore
import pandas as pd
import csv
import datetime
#读取本次目标
store=HDFStore('july.h5')
df=pd.read_csv("75_lightlostuser.csv")

with open("75pushed.csv") as f:
    spamreader = csv.reader(f, delimiter=',')
    pushed=list(spamreader)[0]
print("历史已经推送:", len(pushed))

def if_in(row,list):
    if str(row["id"]) in list:
        return 0
    else:
        return 1

df["if_keep"]= df.apply(lambda row: if_in(row,pushed), axis=1)
df=df.loc[df["if_keep"]==0]
df=df.drop("if_keep",1)
print("仅留push的:",df.shape[0])

df=df.fillna(0)
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index) - df['last']).astype('timedelta64[D]').astype('int')
df["num"]=df["num"].astype(int)
df["if_one_day"]= df['first_order_interval'] == df['last_order_interval']

print(df["if_one_day"].value_counts())

df1=pd.read_csv("75_real_single1.csv")
df2=pd.read_csv("75_real_single2.csv")
df3=pd.read_csv("75_real_normal.csv")
def label_plan(row):
    if row["id"] in df1["userid"].tolist():
        return "1"
    elif row["id"] in df2["userid"].tolist():
        return "2"
    elif row["id"] in df3["userid"].tolist():
        return "3"
    else:
        0
#加入分组标签
df["plan"]=df.apply(lambda row:label_plan(row), axis=1)
print(df["plan"].value_counts())
print(df.shape[0])
#store.put('df_75_all',df,format="table")
store.close()
