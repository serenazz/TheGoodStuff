from pandas import HDFStore
import pandas as pd

store=HDFStore('july.h5')
df1=store['df_75_afterpush']
print(df1)
#添加推送后,取消关注情况
#df_canceld=pd.read_csv("canceled.csv")
#canceled=df_canceld["id"].tolist()


#获取点击/购买名单
clicked=pd.read_csv("7576clicked.csv", delimiter="\n")
bought=pd.read_csv("75D1_bought.csv")
bought=bought["id"].tolist()
clicked=clicked["id"].tolist()
for index in range(len(bought)):
    bought[index]=int(bought[index])
for index in range(len(clicked)):
    clicked[index]=int(clicked[index])
#添加各行为字段
def label_action(row,action):
    count=action.count(row["id"])
    return count
df1["clicked"]=df1.apply(lambda row:label_action(row,clicked), axis=1)
df1["bought"]=df1.apply(lambda row:label_action(row,bought), axis=1)
print(df1.head(5))
print("normal:1302","single1:698","single2:737")
#print(df1.loc[(df1["num"]==1)&(df1["plan"]=="single2")].shape[0])
print(df1.loc[(df1["bought"]>0)]["plan"].value_counts())
print(df1.loc[(df1["clicked"]>0)]["plan"].value_counts())