import pandas as pd
from pandas import HDFStore
import datetime
import csv

#生成历史推送过的list
with open("before_710history.csv") as f:
    spamreader = csv.reader(f, delimiter=',')
    history=list(spamreader)[0]
print("历史已经推送:", len(history))

#读取本次目标
store=HDFStore('july.h5')
df=pd.read_csv("710_lightlost.csv")
print("710三个月内没买:",df.shape[0])

#剔除已推过
def if_in(row,list):
    if str(row["id"]) in list:
        return 0
    else:
        return 1

df["if_keep"]= df.apply(lambda row: if_in(row,history), axis=1)
df=df.loc[df["if_keep"]==1]
df=df.drop("if_keep",1)
print("踢出过历史后:",df.shape[0])


#整理数据
df=df.fillna(0)
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index) - df['last']).astype('timedelta64[D]').astype('int')
df["num"]=df["num"].astype(int)
df["if_one_day"]= df['first_order_interval'] == df['last_order_interval']

print("所有单天用户",df.loc[df["if_one_day"]==True].shape[0])
#print(df["num"].value_counts())
#print(df["num"].describe())
df_single=df.loc[df["if_one_day"]==True]
df_normal=df.loc[df["if_one_day"]==False]
#df_value=df.loc[df["num"]>5]
#df_normal_heavy=df.loc[df["num"]<=5]
#print("五单以上重流失",df_value.shape[0])
#df_normal_heavy=df_normal_heavy.sample(frac=0.2)
#print("普通重流失",df_normal_heavy.shape[0])



single_push1=df_single.sample(frac=0.35)
#single_push2=df_single.drop(single_push1.index).sample(frac=0.3)
normal_push=df_normal.sample(frac=0.4)
print("单天一",single_push1.shape[0])
#print("单天二",single_push2.shape[0])
print("多天:",normal_push.shape[0])

'''
with open("heavy_value.csv",'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(df_value["id"].tolist())

with open("heavy_normal.csv",'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(df_normal_heavy["id"].tolist())

with open("710normal.csv",'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(normal_push["id"].tolist())

with open("710single1.csv",'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(single_push1["id"].tolist())
'''

#store.put('df_710_all',df,format="table")
#store.close()

'''
#创建推送成功df
df["if_keep"]= df.apply(lambda row: if_in(row,pushed_list), axis=1)
df=df.loc[df["if_keep"]==0]
print(df["if_keep"].value_counts())
df_pushed=df.drop("if_keep",1)
#store.put('622pushed',df_pushed,format="table")
print(df_pushed.head(5))
'''