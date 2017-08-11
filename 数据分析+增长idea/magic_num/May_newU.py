import pandas as pd
import datetime
df=pd.read_csv("May_newUser.csv")
df=df.fillna(0)
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['order']=pd.to_datetime(df['order'],format ="%Y-%m-%d")


#是否n天内的订单
def if_n_days(row,n):
    if row["order"]=="1970-01-01":
        return 0
    elif row["order"]<=(row["first"]+datetime.timedelta(days=n)):
        return 1
    else:
        return 0
#是否n天后的订单
def if_after_n_days(row,n):
    if row["order"]=="1970-01-01":
        return 0
    elif row["order"]>(row["first"]+datetime.timedelta(days=n)):
        return 1
    else:
        return 0

df["if_7_days"]=df.apply(lambda row: if_n_days(row,14),axis=1)
df["if_30_days"]=df.apply(lambda row: if_after_n_days(row,30),axis=1)

df["minimum"]=df.groupby(df["id"])[["if_7_days"]].transform('sum')
df["gap"]=(df["order"]-df["first"]).astype('timedelta64[D]').astype('int')
df["first_second_gap"]=df.loc[df["gap"]>=0].groupby("id")["gap"].transform('min')


#创建unique用户的列表
df1=df.drop_duplicates(["id"])
print("描述前两单前间隔","\n",df1["first_second_gap"].describe())
#print("间隔数layout","\n",df1["first_second_gap"].value_counts())
print("总共该月新加入数",df1.shape[0])
print("没有第二单的用户数:",df1.loc[df1["first_second_gap"].isnull() ].shape[0])


#df2=df1.loc[df1["order"]=="1970-01-01"]
df2=df1.copy()
print(df2.first_name.value_counts())
print("第一次用券人数:","\n",df2.first_c.value_counts())


#算前三单都用券用户
df=df.sort_values(["id","order"],ascending=[True,True])
coupon_times=[0]*20
count=0
prev=0
rows=0
if_continue=0
for index, row in df.iterrows():
    if row["id"]!=prev:
        coupon_times[count]+=1
        if row["first_c"]==1 and row["normal_c"]==1:
            if_continue=0
            count=2
        else:
            if_continue=1
            count=0
    else:
        if if_continue==1:
            continue
        elif row["normal_c"]!=1:
            if_continue=1
            continue
        else:
            if row["first_c"]==1 and row["normal_c"]==1:
                if_continue=0
                count+=1
    prev=row["id"]

print(coupon_times)

#算前两单复购率
if_repeat={"repeat":0,"different":0}
if_newid=True
prev=0
for index, row in df.iterrows():
    if row["id"]!=prev:
        if row["normal_name"]== 0:
            continue
        else:
            if row["first_name"]==row["normal_name"]:
                if_repeat["repeat"]+=1
            else:
                if_repeat["different"]+=1
        prev=row["id"]

for key,value in if_repeat.items():
    print(key,value)


#显示至少几单和次月留存关联
print("".join(str(word).ljust(10) for word in ["至少几单","符合","回购但不符合","重合","重合比例"]))
for i in range(1,10):
    min=df.loc[df["minimum"]>=i]["id"].unique().shape[0]
    retained_not_min=df.loc[(df["if_30_days"]>0)&(df["minimum"]<i)]["id"].unique().shape[0]
    overlap=df.loc[(df["minimum"]>=i)&(df["if_30_days"]>0)]["id"].unique().shape[0]
    print("   ".join(str(word).ljust(10) for word in [i,min,retained_not_min,overlap,overlap/(min+retained_not_min)]))





