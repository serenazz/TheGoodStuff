import pandas as pd
import csv
df=pd.read_csv("original_data.csv")
user_info=pd.read_csv("user_info.csv")


'''
with open("user_list.csv","w") as f:
    writer=csv.writer(f)
    writer.writerow(df["id"].tolist())
'''

df=df.merge(user_info,how="left", on="id")
user_info["c_ratio"]=user_info["c_cnt"]/df["num"]
user_info["ratio"]=user_info["p_cnt"]/user_info["num"]
def check_price_sen(row):
    if (row["ratio"]>0.5) or (row["c_ratio"]>0.5):
        return True
    else:
        return False
user_info["price_sen"]= user_info.apply(lambda row: check_price_sen(row), axis=1)
df1=df.copy()
test=user_info["num"].value_counts().to_frame().reset_index().rename(columns={"index":"num","num":"cnt"})
print(test)
test["weight"]=test["num"]*test["cnt"]
print("平均下单数:",test["weight"].sum()/test["cnt"].sum())
print("价格敏感分布: ", "\n",user_info["price_sen"].value_counts())
print(user_info.loc[user_info["id"]==user_info["leaderid"]].shape[0]/user_info.shape[0])
print(df1.loc[df1["num"]==1]["merchid"].value_counts())




'''
df_count=df.groupby('id').merchid.nunique().to_frame().reset_index().rename(columns={'id':'id',"merchid":'cnt'})
print("重复购买分布:","\n",df_count["cnt"].value_counts())
df=df.merge(df_count, how="left",on="id")
print(df.loc[df["cnt"]>1])
target=df.loc[df["cnt"]>1]
target.to_csv("repeated",sep=',',index=False)


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
print(df_f11.shape[0])
#store.put('df_final',df1,format="table")
'''