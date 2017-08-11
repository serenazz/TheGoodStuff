import pandas as pd
from pandas import HDFStore
import csv

'''prepare data'''
#获取推送大表
store=HDFStore('storage1.h5')
df1=store['622pushed']

df1["if_new"]= df1['first_order_interval'] == df1['last_order_interval']

# 标记已推用户
pushed=[]
with open("6.22_guanzhu.csv","r") as f:
    reader=csv.reader(f)
    for i in reader:
        pushed.append(i)
pushed=pushed[0]

for i in range(len(pushed)):
    pushed[i]=int(pushed[i])
def if_in(row,action):
    if row["id"] in action:
        return 1
    else:
        return 0
df1["pushed"]=df1.apply(lambda row: if_in(row,pushed),axis=1)
df1=df1.loc[df1["pushed"]>0]



#添加推送后,取消关注情况
#df_canceld=pd.read_csv("canceled.csv")
#canceled=df_canceld["id"].tolist()


#获取点击/购买名单
clicked=pd.read_csv("622clicked.csv", delimiter="\n")
bought=pd.read_csv("623bought.csv")
bought=bought["id"].tolist()
clicked=clicked["id"].tolist()
for index in range(len(clicked)):
    clicked[index]=int(clicked[index])

#添加各行为字段
def label_action(row,action):
    count=action.count(row["id"])
    return count
df1["clicked"]=df1.apply(lambda row:label_action(row,clicked), axis=1)
df1["bought"]=df1.apply(lambda row:label_action(row,bought), axis=1)
test=df1.loc[df1["bought"]>0]

#df1["canceled"]=df1.apply(lambda row:label_action(row,canceled), axis=1)
#df1["bought_1D"]=df1.apply(lambda row: label_action(row,bought_1D),axis=1)




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






print("==================以下为点击数据================")
print("多天: ",df_f2.loc[(df_f2["clicked"]>0)].shape[0]/df_f2.shape[0])
print("单天1单: ",df_f5.loc[(df_f5["clicked"]>0)].shape[0]/df_f5.shape[0])
print("单天多单: ",df_f6.loc[(df_f6["clicked"]>0)].shape[0]/df_f6.shape[0])
print("新用户: ",df_f3.loc[(df_f3["clicked"]>0)].shape[0]/df_f3.shape[0])
print("老用户: ",df_f4.loc[(df_f4["clicked"]>0)].shape[0]/df_f4.shape[0])
print("轻流失: ",df_f10.loc[(df_f10["clicked"]>0)].shape[0]/df_f10.shape[0])
#print("重流失: ",df_f11.loc[(df_f11["clicked"]>0)].shape[0]/df_f11.shape[0])
print("敏感: ", df1.loc[(df1["clicked"]>0)&(df1["price_sen"]==True)].shape[0]/(df1.loc[(df1["price_sen"]==True),:].shape[0]))
print("不敏感: ", df1.loc[(df1["clicked"]>0)&(df1["price_sen"]==False)].shape[0]/(df1.loc[(df1["price_sen"]==False),:].shape[0]))
print()
'''
print("==================以下为购买数据================")
print("多天: ",df_f2.loc[df_f2["bought"]>0].shape[0],(df_f2.loc[df_f2["bought"]>0].shape[0])/df_f2.shape[0], ",",df_f2["bought"].sum())
print("单天1单: ",df_f5.loc[(df_f5["bought"]>0)].shape[0],(df_f5.loc[(df_f5["bought"]>0)].shape[0])/df_f5.shape[0],",",df_f5["bought"].sum())
print("单天多单: ",df_f6.loc[(df_f6["bought"]>0)].shape[0],(df_f6.loc[(df_f6["bought"]>0)].shape[0])/df_f6.shape[0],",",df_f6["bought"].sum())
print("新用户: ",df_f3.loc[(df_f3["bought"]>0)].shape[0],(df_f3.loc[(df_f3["bought"]>0)].shape[0])/df_f3.shape[0],",",df_f3["bought"].sum())
print("老用户: ",df_f4.loc[(df_f4["bought"]>0)].shape[0],(df_f4.loc[(df_f4["bought"]>0)].shape[0])/df_f4.shape[0],",",df_f4["bought"].sum())
print("轻流失: ",df_f10.loc[(df_f10["bought"]>0)].shape[0],(df_f10.loc[(df_f10["bought"]>0)].shape[0])/df_f10.shape[0],",",df_f10["bought"].sum())
#print("重流失: ",(df_f11.loc[(df_f11["bought"]>0)].shape[0])/df_f11.shape[0],",",df_f11["bought"].sum())
print("敏感: ", df1.loc[(df1["bought"]>0)&(df1["price_sen"]==True)].shape[0],(df1.loc[(df1["bought"]>0)&(df1["price_sen"]==True)].shape[0])/(df1.loc[(df1["price_sen"]==True),:].shape[0]),",",df1.loc[(df1["price_sen"]==True)]["bought"].sum())
print("不敏感: ", df1.loc[(df1["bought"]>0)&(df1["price_sen"]==False)].shape[0],(df1.loc[(df1["bought"]>0)&(df1["price_sen"]==False)].shape[0])/(df1.loc[(df1["price_sen"]==False),:].shape[0]),",",df1.loc[(df1["price_sen"]==False)]["bought"].sum())
print()
print()
'''
