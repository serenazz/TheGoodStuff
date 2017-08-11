import pandas as pd
import matplotlib.pyplot as plt
import csv
import datetime

#read data
df = pd.read_csv("promotion_preferred_users.csv")
df_user=pd.read_csv("high_rate_promotion>=1.csv")

#configure time
df_user=df_user.fillna(0)
df_user.first=df_user["first"].replace({0 :"2000-1-1"})
df_user.last=df_user["last"].replace({0 :"2000-1-1"})
df_user['first']=pd.to_datetime(df_user['first'],format ="%Y-%m-%d")
df_user['last']=pd.to_datetime(df_user['last'],format ="%Y-%m-%d")

df_user['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index)- df_user['first']).astype('timedelta64[D]')
df_user['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index)- df_user['last']).astype('timedelta64[D]')

#cleaning data & adding metrics
df["userid"]=df["userid"].astype('int')
df["promotion_ratio"]=df.promotion_cnt/df.total_cnt
df=df.sort_values("promotion_ratio", ascending= False)
df["group"]=df["promotion_ratio"]//0.1

##plot overall histogram
df["promotion_ratio"].plot.hist(alpha=0.5)
df["promotion_cnt"]=df["promotion_cnt"].astype('int')
df["promotion_amt"]=df["promotion_amt"].astype('int')
plt.xlabel("promotion_cnt/total_cnt")
plt.ylabel("number of users")
plt.show()

#focus analyzing on high promotion ratio users
df1=df[df.promotion_ratio==1]
df2=df1[df1.promotion_cnt >1]
df2=df2.sort_values("total_cnt", ascending= False)
df_merge=pd.merge(df2, df_user, how='inner', left_on="userid",right_on="userid")
df2=df2.as_matrix()

df_merge=df_merge[df_merge.first_order_interval<=600]
df_merge=df_merge[df_merge.last_order_interval<=600]
'''
df3=df_merge.as_matrix()
plt.plot(df3[:,-2],df3[:,-1],'o')
plt.show()
'''

print("最多买过, ",max(df2[:,2]))
print("买过的人有: ",df2.shape[0])

'''
with open('promotion_user_list.csv','w',encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(df2[:,0])
'''
