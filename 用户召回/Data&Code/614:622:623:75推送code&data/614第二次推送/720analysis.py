import pandas as pd
import datetime
import csv
store=pd.HDFStore('storage1.h5')
#添加coupon ratio column
df=pd.read_csv("lost_users.csv")
#df=df.dropna()
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (datetime.datetime(2017, 6, 14) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(datetime.datetime(2017, 6, 14) - df['last']).astype('timedelta64[D]').astype('int')
df=df.sort_values(by="last_order_interval")
df["recently_joined"]=df["first_order_interval"]<=90
df["ratio"]=df.promotion_cnt/df.num
df=df.loc[(df["last_order_interval"]<=90)&(df["last_order_interval"]>30)]
df1=df
df1["if_new"]= df1['first_order_interval'] == df1['last_order_interval']

#添加各用户优惠券使用情况
df_coupon=pd.read_csv("coupon.csv")
df1=df1.merge(df_coupon,how="left",on="id")
df1["c_ratio"]=df1["coupon_cnt"]/df1["num"]
def check_price_sen(row):
    if (row["ratio"]>0.5) or (row["c_ratio"]>0.5):
        return True
    else:
        return False
df1["price_sen"]= df1.apply(lambda row: check_price_sen(row), axis=1)
pushed=[]
with open("sent.csv","r") as f:
    reader=csv.reader(f)
    for i in reader:
        pushed.append(i)
pushed=pushed[0]
for i in range(len(pushed)):
    pushed[i]=int(pushed[i])

succeeded=[]
with open("pushed.csv","r") as f:
    reader=csv.reader(f)
    for i in reader:
        succeeded.append(i)
succeeded=succeeded[0]
for i in range(len(succeeded)):
    succeeded[i]=int(succeeded[i])

def if_in(row,list1,list2):
    if row["id"] in list2:
        return 1
    elif row["id"] in list1:
        return 0
    else:
        return 2

df1["pushed"]=df1.apply(lambda row: if_in(row,pushed,succeeded),axis=1)
print(df1["pushed"].value_counts())

plan1=pd.read_csv("plan1g.csv",delimiter="\n")
plan2=pd.read_csv("plan2g.csv",delimiter="\n")
plan3=pd.read_csv("plan3g.csv",delimiter="\n")
plan4=pd.read_csv("plan4g.csv",delimiter="\n")

lplan1=plan1["userid"].tolist()
lplan2=plan2["userid"].tolist()
lplan3=plan3["userid"].tolist()
lplan4=plan4["userid"].tolist()

def label_plan(row):
    if row["id"] in lplan1:
        return 1
    elif row["id"] in lplan2:
        return 2
    elif row["id"] in lplan3:
        return 3
    elif row["id"] in lplan4:
        return 4
    else:
        0
df1["plan"]=df1.apply(lambda row: label_plan(row),axis=1)

#获取所有流失用户30天购买名单
bought=pd.read_csv("after_30days.csv")
bought=bought["id"].tolist()
print("三十天内共多少单",len(bought))
print("三个月加入用户分布",df1["if_new"].value_counts())
#添加各行为字段
def label_action(row,action):
    count=action.count(row["id"])
    return count

df1["bought"]=df1.apply(lambda row:label_action(row,bought), axis=1)
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

print(df1["price_sen"].value_counts())
push=[1]
plan=[1,3,4,2]
print(df1["plan"].value_counts())
for i in push:
    for n in plan:
        print("push: ",i,"plan: ",n)
        fi_num=df1.loc[(df1["pushed"]==i)&(df1["plan"]==n)].shape[0]
        print(fi_num)
        print((df1.loc[(df1["bought"]>0)&(df1["pushed"]==i)&(df1["plan"]==n)].shape[0])/fi_num, ",",df1.loc[(df1["pushed"]==i)&(df1["plan"]==n)]["bought"].sum()/fi_num)
comparison_num=df1.loc[(df1["pushed"]==2)].shape[0]
print(df1.loc[(df1["bought"]>0)&(df1["pushed"]==2)].shape[0]/comparison_num, ",",df1.loc[(df1["pushed"]==2)]["bought"].sum()/comparison_num)
'''
print("==================以下为购买数据================")
for i in pushed:
    print(i)
    f2_num=df_f2.loc[(df_f2["pushed"]==i)].shape[0]
    f5_num=df_f5.loc[(df_f5["pushed"]==i)].shape[0]
    f6_num=df_f6.loc[(df_f6["pushed"]==i)].shape[0]
    f3_num=df_f3.loc[(df_f3["pushed"]==i)].shape[0]
    f4_num=df_f4.loc[(df_f4["pushed"]==i)].shape[0]
    f10_num=df_f10.loc[(df_f10["pushed"]==i)].shape[0]
    f11_num=df_f11.loc[(df_f11["pushed"]==i)].shape[0]
    f12_num=df1.loc[(df1["price_sen"]==True)&(df1["pushed"]==i)].shape[0]
    f13_num=df1.loc[(df1["price_sen"]==False)&(df1["pushed"]==i)].shape[0]
    print("多天: ",(df_f2.loc[(df_f2["bought"]>0)&(df_f2["pushed"]==i)].shape[0])/f2_num, ",",df_f2.loc[df_f2["pushed"]==i]["bought"].sum()/f2_num)
    print("单天1单: ",df_f5.loc[(df_f5["pushed"]==i)&(df_f5["bought"]>0)].shape[0]/f5_num,",",df_f5.loc[df_f5["pushed"]==i]["bought"].sum()/f5_num)
    print("单天多单: ",df_f6.loc[(df_f6["pushed"]==i)&(df_f6["bought"]>0)].shape[0]/f6_num,",",df_f6.loc[df_f6["pushed"]==i]["bought"].sum()/f6_num)
    print("新用户: ",df_f3.loc[(df_f3["pushed"]==i)&(df_f3["bought"]>0)].shape[0]/f3_num,",",df_f3.loc[df_f3["pushed"]==i]["bought"].sum()/f3_num)
    print("老用户: ",df_f4.loc[(df_f4["pushed"]==i)&(df_f4["bought"]>0)].shape[0]/f4_num,",",df_f4.loc[df_f4["pushed"]==i]["bought"].sum()/f4_num)
    print("轻流失: ",df_f10.loc[(df_f10["pushed"]==i)&(df_f10["bought"]>0)].shape[0]/f10_num,",",df_f10.loc[df_f10["pushed"]==i]["bought"].sum()/f10_num)
    print("重流失: ",df_f11.loc[(df_f11["pushed"]==i)&(df_f11["bought"]>0)].shape[0]/f11_num,",",df_f11.loc[df_f11["pushed"]==i]["bought"].sum()/f11_num)
    print("敏感: ", df1.loc[(df1["pushed"]==i)&(df1["bought"]>0)&(df1["price_sen"]==True)].shape[0]/f12_num,",",df1.loc[(df1["pushed"]==i)&(df1["price_sen"]==True)]["bought"].sum()/f12_num)
    print("不敏感: ", df1.loc[(df1["pushed"]==i)&(df1["bought"]>0)&(df1["price_sen"]==False)].shape[0]/f13_num,",",df1.loc[(df1["pushed"]==i)&(df1["price_sen"]==False)]["bought"].sum()/f13_num)
    print()
    print()
'''