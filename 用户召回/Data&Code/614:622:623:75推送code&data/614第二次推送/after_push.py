import pandas as pd
from pandas import HDFStore
import csv

'''prepare data'''
#获取推送大表
store=HDFStore('storage1.h5')
df1=store['df_final']
'''
#添加各用户优惠券使用情况
df_coupon=pd.read_csv("coupon.csv")
df1=df1.merge(df_coupon,how="left",on="id")
'''
#添加推送后,取消关注情况
df_canceld=pd.read_csv("canceled.csv")
canceled=df_canceld["id"].tolist()

#清洗整理数据
df1=df1.fillna(0)
df1["c_ratio"]=df1["coupon_cnt"]/df1["num"]
#df1=df1.drop("regular_cnt",1)
#df1=df1.drop("regular_amt",1)

pushed=[]
with open("pushed.csv","r") as f:
    reader=csv.reader(f)
    for i in reader:
        pushed.append(i)
pushed=pushed[0]
for i in range(len(pushed)):
    pushed[i]=int(pushed[i])


#获取点击/购买名单
clicked=pd.read_csv("clicked_48Hr.csv", delimiter="\n")
bought=pd.read_csv("Day3bought"
                   ".csv")
bought=bought["id"].tolist()
bought_1D=pd.read_csv("bought_D5.csv")
bought_1D=bought_1D["id"].tolist()
clicked=clicked["id"].tolist()

def if_in(row,action):
    if row["id"] in action:
        return 1
    else:
        return 0

#添加各行为字段
def label_action(row,action):
    count=action.count(row["id"])
    return count
#df1["clicked"]=df1.apply(lambda row:label_action(row,clicked), axis=1)
df1["bought"]=df1.apply(lambda row:label_action(row,bought), axis=1)
df1["canceled"]=df1.apply(lambda row:label_action(row,canceled), axis=1)
df1["bought_1D"]=df1.apply(lambda row: label_action(row,bought_1D),axis=1)
df1["pushed"]=df1.apply(lambda row: if_in(row,pushed),axis=1)
#定义各类用户
#单天用户
df_f1=df1.loc[(df1["if_new"]==True),:]
#单天一单
df_f5=df_f1.loc[df_f1["num"]==1,:]
#单天多单
df_f6=df_f1.loc[df_f1["num"]>1,:]
#多天用户
df_f2=df1.loc[(df1["if_new"]==False),:]
#新用户
df_f3=df1.loc[(df1["recently_joined"]==True),:]
#老用户
df_f4=df1.loc[(df1["recently_joined"]==False),:]
#轻流失
df_f10=df1.loc[(df1["last_order_interval"]<=60),:]
#重流失
df_f11=df1.loc[(df1["last_order_interval"]>60),:]
#store.put('df_final',df1,format="table")
'''
print("==================以下为点击数据================")
for i in range(1,5):
    print("plan",i)
    print("多天: ",df_f2.loc[(df_f2["clicked"]>0)&(df_f2["plan"]==i)].shape[0])
    print("单天1单: ",df_f5.loc[(df_f5["plan"]==i)&(df_f5["clicked"]>0)].shape[0])
    print("单天多单: ",df_f6.loc[(df_f6["plan"]==i)&(df_f6["clicked"]>0)].shape[0])
    print("新用户: ",df_f3.loc[(df_f3["plan"]==i)&(df_f3["clicked"]>0)].shape[0])
    print("老用户: ",df_f4.loc[(df_f4["plan"]==i)&(df_f4["clicked"]>0)].shape[0])
    print("轻流失: ",df_f10.loc[(df_f10["plan"]==i)&(df_f10["clicked"]>0)].shape[0])
    print("重流失: ",df_f11.loc[(df_f11["plan"]==i)&(df_f11["clicked"]>0)].shape[0])
    print("敏感: ", df1.loc[(df1["plan"]==i)&(df1["clicked"]>0)&(df1["price_sen"]==True)].shape[0])
    print("不敏感: ", df1.loc[(df1["plan"]==i)&(df1["clicked"]>0)&(df1["price_sen"]==False)].shape[0])
    print()
'''
print("==================以下为购买数据================")
for i in range(1,5):
    print("plan",i)
    f2_num=df_f2.loc[(df_f2["plan"]==i)&(df_f2["pushed"]>0)].shape[0]
    f5_num=df_f5.loc[(df_f5["plan"]==i)&(df_f5["pushed"]>0)].shape[0]
    print("多天: ",(df_f2.loc[(df_f2["bought"]>0)&(df_f2["plan"]==i)].shape[0])/f2_num, ",",df_f2.loc[df_f2["plan"]==i]["bought"].sum())
    print("单天1单: ",df_f5.loc[(df_f5["plan"]==i)&(df_f5["bought"]>0)].shape[0]/f5_num,",",df_f5.loc[df_f5["plan"]==i]["bought"].sum())
    print("单天多单: ",df_f6.loc[(df_f6["plan"]==i)&(df_f6["bought"]>0)].shape[0],",",df_f6.loc[df_f6["plan"]==i]["bought"].sum())
    print("新用户: ",df_f3.loc[(df_f3["plan"]==i)&(df_f3["bought"]>0)].shape[0],",",df_f3.loc[df_f3["plan"]==i]["bought"].sum())
    print("老用户: ",df_f4.loc[(df_f4["plan"]==i)&(df_f4["bought"]>0)].shape[0],",",df_f4.loc[df_f4["plan"]==i]["bought"].sum())
    print("轻流失: ",df_f10.loc[(df_f10["plan"]==i)&(df_f10["bought"]>0)].shape[0],",",df_f10.loc[df_f10["plan"]==i]["bought"].sum())
    print("重流失: ",df_f11.loc[(df_f11["plan"]==i)&(df_f11["bought"]>0)].shape[0],",",df_f11.loc[df_f11["plan"]==i]["bought"].sum())
    print("敏感: ", df1.loc[(df1["plan"]==i)&(df1["bought"]>0)&(df1["price_sen"]==True)].shape[0],",",df1.loc[(df1["plan"]==i)&(df1["price_sen"]==True)]["bought"].sum())
    print("不敏感: ", df1.loc[(df1["plan"]==i)&(df1["bought"]>0)&(df1["price_sen"]==False)].shape[0],",",df1.loc[(df1["plan"]==i)&(df1["price_sen"]==False)]["bought"].sum())
    print()
    print()
#print(df1.loc[(df1["plan"]==i)&(df1["bought"]>0)&(df1["price_sen"]==False)])
#print(df_f10.loc[(df_f10["plan"]==i)&(df_f10["bought"]>0)])


