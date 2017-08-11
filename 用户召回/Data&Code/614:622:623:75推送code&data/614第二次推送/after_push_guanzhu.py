import pandas as pd
from pandas import HDFStore

#load data
store=HDFStore('storage1.h5')
df1=store['df_with_plan']
df_coupon=pd.read_csv("coupon.csv")
df1=df1.merge(df_coupon,how="left",on="id")
df1=df1.fillna(0)
df1["c_ratio"]=df1["coupon_cnt"]/df1["num"]

def check_price_sen(row):
    if (row["ratio"]>0.5) or (row["c_ratio"]>0.5):
        return True
    else:
        return False
df1["price_sen"]= df1.apply(lambda row: check_price_sen(row), axis=1)



print("===========以下为关注数据================")
#导入关注名单
followed=[]
plan1g=pd.read_csv("plan1g.csv",delimiter="\n")
followed=plan1g["userid"].tolist()
plan2g=pd.read_csv("plan2g.csv",delimiter="\n")
plan3g=pd.read_csv("plan3g.csv",delimiter="\n")
plan4g=pd.read_csv("plan4g.csv",delimiter="\n")
for i in plan2g["userid"].tolist():
    followed.append(i)
for i in plan3g["userid"].tolist():
    followed.append(i)
for i in plan4g["userid"].tolist():
    followed.append(i)
#添加关注标签到总推送表
def label_plan(row,plan):
    if row["id"] in plan:
        return True
    else:
        return False
df1["follow"]= df1.apply(lambda row:label_plan(row,followed), axis=1)

#单天用户
df_f1=df1.loc[(df1["if_new"]==True),:]
#单天用户-一单
df_f5=df_f1.loc[df_f1["num"]==1,:]
#丹田用户-多单
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
print("共",len(followed),"关注")
'''
生成推送成功的名单,以便sql查询
with open("pushed.csv","w") as f:
    spamwriter = csv.writer(f, delimiter=',')
    spamwriter.writerow(followed)
'''
print("单天用户是否关注: ", '\n',df_f1["follow"].value_counts())
print("多天用户是否关注: ",'\n', df_f2["follow"].value_counts())
print("新用户是否关注: ", '\n',df_f3["follow"].value_counts())
print("老用户是否关注: ", '\n',df_f4["follow"].value_counts())
print("轻流失是否关注: ",'\n',df_f10["follow"].value_counts())
print("重流失是否关注: ",'\n',df_f11["follow"].value_counts())

'''
print("==========以下为方案各用户组总人数===============")
for i in range(1,5):
    print("plan",i)
    print("多天: ",df_f2.loc[(df_f2["plan"]==i)&(df_f2["follow"]==True)].shape[0])
    print("===价格敏感",df_f2.loc[(df_f2["plan"]==i)&(df_f2["follow"]==True)&(df_f2["price_sen"]==True)].shape[0])
    print("单天1单: ",df_f5.loc[(df_f5["plan"]==i)&(df_f5["follow"]==True)].shape[0])
    print("===价格敏感",df_f5.loc[(df_f5["plan"]==i)&(df_f5["follow"]==True)&(df_f5["price_sen"]==True)].shape[0])
    print("单天多单: ",df_f6.loc[(df_f6["plan"]==i)&(df_f6["follow"]==True)].shape[0])
    print("===价格敏感",df_f6.loc[(df_f6["plan"]==i)&(df_f6["follow"]==True)&(df_f6["price_sen"]==True)].shape[0])
    print("新用户: ",df_f3.loc[(df_f3["plan"]==i)&(df_f3["follow"]==True)].shape[0])
    print("老用户: ",df_f4.loc[(df_f4["plan"]==i)&(df_f4["follow"]==True)].shape[0])
    print("轻流失: ",df_f10.loc[(df_f10["plan"]==i)&(df_f10["follow"]==True)].shape[0])
    print("重流失: ",df_f11.loc[(df_f11["plan"]==i)&(df_f11["follow"]==True)].shape[0])
    print("敏感: ", df1.loc[(df1["plan"]==i)&(df1["follow"]==True)&(df1["price_sen"]==True)].shape[0])
    print("不敏感: ", df1.loc[(df1["plan"]==i)&(df1["follow"]==True)&(df1["price_sen"]==False)].shape[0])
    print()
'''