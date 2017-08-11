import pandas as pd
from pandas import HDFStore
from datetime import datetime

store = HDFStore('storage1.h5')
df1= store["pushed_browse"]
all=store["df_final"]


D1=df1.loc[df1["time"]<datetime.strptime("2017-06-15 13:30:00",'%Y-%m-%d %H:%M:%S')]
D2=df1.loc[df1["time"]>datetime.strptime("2017-06-15 12:30:00",'%Y-%m-%d %H:%M:%S')]
D2=D2.loc[df1["time"]<datetime.strptime("2017-06-16 12:30:00",'%Y-%m-%d %H:%M:%S')]
D1m=D1.merge(all,how="left",left_on="userid",right_on="id")
D2m=D2.merge(all,how="left",left_on="userid",right_on="id")
count=D1.loc[D1["url"]=="商品详情"].groupby("userid").size().to_frame().reset_index().rename(columns={'userid':'id',0:'records'})
merged=all.merge(count,how="left", on="id")



df1["sub1"],df1["sub2"]=df1["suburl"].str.split("&",1).str
print(df1.shape[0])
userlist=[]
userdic={}
for index, row in df1.iterrows():
    id=df1.iloc[index]["userid"]
    if id in userlist:
        pass
    else:
        userlist.append(id)
    if df1.iloc[index]["url"]=="我的好东西":
        if df1.iloc[index]["userid"] in userdic:
            continue
        else:
            userdic[id]=0
            continue

    if (id in userdic) and userdic[id]==0:
        if df1.iloc[index]["url"]=="邀请参团":
            userdic[id]=1
        #elif df1.iloc[index]["url"]=="优惠券":
            #userdic[id]=0
        #elif df1.iloc[index]["url"]=="抢优惠劵":
            #userdic[id]=0
            #continue
        else:
            print("没去首页%%%%%%%%%%%%%%%%%%%%:")
            userdic[id]=-1
            print(df1.iloc[index]["time"],df1.iloc[index]["userid"],df1.iloc[index]["url"],df1.iloc[index]["suburl"])
    else:
        continue

c_noaction=0
c_shouye=0
c_other=0
el=0
for key, value in userdic.items():
    if userdic[key]==0:
        c_noaction+=1
    elif userdic[key]==1:
        c_shouye+=1
    elif userdic[key]==-1:
        c_other+=1
    else:
        el+=1

print(len(userlist))
print(c_noaction,c_shouye,c_other,el)


#单天用户
df_f1=merged.loc[(merged["if_new"]==True),:]
#单天一单
df_f5=df_f1.loc[df_f1["num"]==1,:]
#单天多单
df_f6=df_f1.loc[df_f1["num"]>1,:]
#多天用户
df_f2=merged.loc[(merged["if_new"]==False),:]
#新用户
df_f3=merged.loc[(merged["recently_joined"]==True),:]
#老用户
df_f4=merged.loc[(merged["recently_joined"]==False),:]
#轻流失
df_f10=merged.loc[(merged["last_order_interval"]<=60),:]
#重流失
df_f11=merged.loc[(merged["last_order_interval"]>60),:]
'''
for i in range(1,5):
    print("plan",i)
    print("多天: ","\n",df_f2.loc[(df_f2["plan"]==i)]["records"].value_counts())
    print("单天1单: ","\n",df_f5.loc[(df_f5["plan"]==i)]["records"].value_counts())
    print("单天多单: ","\n",df_f6.loc[(df_f6["plan"]==i)]["records"].value_counts())
    print("新用户: ","\n",df_f3.loc[(df_f3["plan"]==i)]["records"].value_counts())
    print("老用户: ","\n",df_f4.loc[(df_f4["plan"]==i)]["records"].value_counts())
    print("轻流失: ","\n",df_f10.loc[(df_f10["plan"]==i)]["records"].value_counts())
    print("重流失: ","\n",df_f11.loc[(df_f11["plan"]==i)]["records"].value_counts())
    print("敏感: ", merged.loc[(merged["plan"]==i)&(merged["price_sen"]==True)]["records"].value_counts())
    print("不敏感: ", merged.loc[(merged["plan"]==i)&(merged["price_sen"]==True)]["records"].value_counts())
    print()
    print()
'''