import pandas as pd
import datetime
import numpy as np
from pandas import HDFStore
#id,first,last,num,userid,total_cnt,promotion_cnt,promotion_amt,regular_cnt,regular_amt
#下次generate前:
#去除历史推送名单
#添加coupon ratio column
df=pd.read_csv("lost_users.csv")
#df=df.dropna()
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index) - df['last']).astype('timedelta64[D]').astype('int')
df=df.sort_values(by="last_order_interval")
df["recently_joined"]=df["first_order_interval"]<=90
df["ratio"]=df.promotion_cnt/df.num
print(df.recently_joined.value_counts())
#导出近期流失用户
#df1=df[df.last_order_interval>=30]
#df1=df1[df1.last_order_interval<90]
df1=df
df1["if_new"]= df1['first_order_interval'] == df1['last_order_interval']
#还可以算再加入后一段时间内下单的,算是新用户也可以

#多余两天购买的用户
df_old_user= df1.loc[df1["if_new"] == False, "id":"ratio"]
df_old_coupon=df_old_user.loc[df_old_user["ratio"]>0.5]
#只购买一天且一次的用户
df_new_single=df1.loc[(df1["if_new"] == True)&(df1["num"]==1), "id":"ratio"]
#只购买一天且多次的用户
df_new_multi= df1.loc[(df1["if_new"] == True)&(df1["num"]>1), "id":"ratio"]




print("流失用户(最后购买在30天外) ", df.shape)
print("最后购买在30-90天内, ", df1.shape)
print()
print("30-90天内老用户买过>=2天, ",df_old_user.shape[0])
print("早加入: ", df_old_user[df_old_user["recently_joined"]==False].shape[0])
print("优惠券高: ", df_old_user.loc[df_old_user["ratio"]>0.5].shape[0])
print()
print("30-90天内新用户一天下多单", df_new_multi.shape[0])
print("优惠券高: ", df_new_multi.loc[df_new_multi["ratio"]>0.5].shape[0])
print()
print("最后购买在30-90天内, 只购买过一次",df_new_single.shape[0])
print("优惠券高: ", df_new_single.loc[df_new_single["ratio"]>0.5].shape[0])
print()
'''
# create (or open) an hdf5 file and opens in append mode
df2=df1.sample(frac=0.2).reset_index(drop=True)
print(df1.shape[0])
print(df2.shape[0])

hdf = HDFStore('store.h5')
hdf.put('df1',df2,format="table")

df_joined_long=df_old_user[df_old_user["recently_joined"]==False]
df_joined_recent=df_old_user[df_old_user["recently_joined"]==True]
df_once= df1.loc[df1["if_new"] == True, "id":"ratio"]

hdf.put('df_old',df_joined_long,format="table")
hdf.put('df_new',df_joined_recent,format="table")
hdf.put('df_once',df_once,format="table")


'''

#查找符合某一特定条件的用户id
#print(df_lost_90_more_time_same_day_order[df_lost_90_more_time_same_day_order["num"]==7]["id"])
''''''

'''#聚类
x=np.array([[60,52],
            [262,67],
            [250,200],
           [300,292]])
#normalize data - no need under this use case
#df1.loc[:,("first_order_interval","last_order_interval")]=(df1.loc[:,("first_order_interval","last_order_interval")]-df1.loc[:,("first_order_interval","last_order_interval")].mean())/(df1.loc[:,("first_order_interval","last_order_interval")].max()-df1.loc[:,("first_order_interval","last_order_interval")].min())


kmeans=KMeans(n_clusters=4).fit(df1.loc[:,["first_order_interval","last_order_interval"]])
labels=kmeans.labels_
centroids = kmeans.cluster_centers_
df2=df1.copy()
df2["group"]=pd.Series(labels,index=df1.index)
print(df2.tail(30000))
#need to install tables module. need space on device
#store = pd.HDFStore('lost_users.h5')
#store.append('users_with_group', df2, data_columns=True)

first_ranked = sorted(centroids[:,0])
last_ranked = sorted(centroids[:,1])
def groupnumis(x):
    if x[0]==first_ranked[0]:
        return 1
    elif x[0]==first_ranked[1]:
        return 2
    else:
        if x[1]==last_ranked[3]:
            return 4
        else:
            return 3
colors=['red', 'blue','yellow',"pink","green"]
for i in range(5):
    ds=df1.as_matrix()[np.where(labels==i)]
    plt.plot(ds[:,4], ds[:,5],'o', color=colors[i],label = "Last: "+ str(ds[0,5]//30)+" to "+str(ds[-1,5]//30)+"; "+ "First: "+str(min(ds[:,4])//30)+" to "+str(max(ds[:,4])//30))
    print("First: ", str(min(ds[:,3])//30),"to ", str(max(ds[:,3])))
    print("groupnum is: ", groupnumis(centroids[i]))
    print("records: ", len(ds[:,0]))
plt.legend(loc = 'upper left')
plt.xlabel('Days Since First Order')
plt.ylabel('Days Since Last Order')
plt.show()
'''




