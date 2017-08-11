import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
df=pd.read_csv("zxs_one_week.csv")
df=df.loc[df["leader_id"]!=0]
#df['first_order']=pd.to_datetime(df['first_order'],format ='%m/%d/%Y')
#df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first_order']).astype('timedelta64[D]').astype('int')


#just analyze level 3,4,5,6
#df=df.loc[(df["rank"]==5)|(df["rank"]==4)|(df["rank"]==6)]

print(df.shape[0])

#df=df.loc[df["last_three_months"]>=50]

print(df.shape[0])
#print(df.first_order_interval.describe())


#print(df.loc[df["leader_id"]==237])
#print(df.new_users.describe())
print(df.first_order.tolist())
print(df["rank"].describe())
print(df.loc[df["last_three_months"]<50].shape[0])



print(df.last_three_months.describe())
groups=pd.cut(df.last_three_months,10)
print(groups.value_counts())
#groups=pd.cut(df.new_users,10)
#print(groups.value_counts())



#print(df.loc[df["last_three_months"]>500].shape[0])
#df.last_three_months.plot.hist(alpha=0.5)
#print(df.loc[df["size_of_group"]<2]["last_three_months"])

'''
df.loc[df["size_of_group"]<=10].size_of_group.plot.hist(alpha=0.5)
plt.show()
'''
#too_small=df.loc[df["size_of_group"]<30]
#print(too_small.head(10))


groups=pd.cut(df.size_of_group,10)
print(groups.value_counts())
for i, row in df.iterrows():
    x= row["last_three_months"]
    y=row["size_of_group"]
    plt.plot(x, y, marker='o',color="green")
plt.xlabel("有效会员数")
plt.ylabel("同类甄选师数")
plt.show()
