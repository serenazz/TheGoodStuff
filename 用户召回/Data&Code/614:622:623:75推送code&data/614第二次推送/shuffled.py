import pandas as pd
from pandas import HDFStore


store=HDFStore('storage1.h5')
df1=store['df1']
df1=df1.drop("userid",1)

#多余两天购买的用户
df_old_user= df1.loc[df1["if_new"] == False, "id":"ratio"]
df_old_coupon=df_old_user.loc[df_old_user["ratio"]>0.5]
#只购买一天且一次的用户
df_new_single=df1.loc[(df1["if_new"] == True)&(df1["num"]==1), "id":"ratio"]
#只购买一天且多次的用户
df_new_multi= df1.loc[(df1["if_new"] == True)&(df1["num"]>1), "id":"ratio"]
'''
#分组
plan1=df1.sample(frac=0.25)
plan2=df1.drop(plan1.index).sample(frac=0.3333333333)
plan3=df1.drop(plan1.index).drop(plan2.index).sample(frac=0.5)
plan4=df1.drop(plan1.index).drop(plan2.index).drop(plan3.index).sample(frac=1)

lplan1=plan1["id"].tolist()
lplan2=plan2["id"].tolist()
lplan3=plan3["id"].tolist()
lplan4=plan4["id"].tolist()

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
#加入分组标签
df1["plan"]=df1.apply(lambda row:label_plan(row), axis=1)
#输出csv文件
plan1["id"].to_frame().to_csv("plan1",sep=',',index=False, line_terminator=',')
plan2["id"].to_frame().to_csv("plan2",sep=',',index=False, line_terminator=',')
plan3["id"].to_frame().to_csv("plan3",sep=',',index=False, line_terminator=',')
plan4["id"].to_frame().to_csv("plan4",sep=',',index=False, line_terminator=',')

store.put('df_with_plan',df1,format="table")


print("each group has X users", plan1.shape[0],plan2.shape[0],plan3.shape[0],plan4.shape[0])
print("plan,>=2,early,high_c, single,single_c")
print("plan1", plan1.loc[plan1["if_new"] == False, "id":"ratio"].shape[0],
      plan1.loc[plan1["if_new"] == False, "id":"ratio"][plan1.loc[plan1["if_new"] == False, "id":"ratio"]["recently_joined"]==False].shape[0],
      plan1.loc[plan1["if_new"] == False, "id":"ratio"].loc[plan1.loc[plan1["if_new"] == False, "id":"ratio"]["ratio"]>0.5].shape[0],
      plan1.loc[(plan1["if_new"] == True)&(plan1["num"]==1), "id":"ratio"].shape[0],
      plan1.loc[(plan1["if_new"] == True)&(plan1["num"]==1)&(plan1["ratio"]>0.5), "id":"ratio"].shape[0],
      plan1.loc[(plan1["if_new"] == True)&(plan1["num"]>1), "id":"ratio"].shape[0],
      plan1.loc[(plan1["if_new"] == True)&(plan1["num"]>1)&(plan1["ratio"]>0.5), "id":"ratio"].shape[0])
print()
print("plan2", plan2.loc[plan2["if_new"] == False, "id":"ratio"].shape[0],
      plan2.loc[plan2["if_new"] == False, "id":"ratio"][plan2.loc[plan2["if_new"] == False, "id":"ratio"]["recently_joined"]==False].shape[0],
      plan2.loc[plan2["if_new"] == False, "id":"ratio"].loc[plan2.loc[plan2["if_new"] == False, "id":"ratio"]["ratio"]>0.5].shape[0],
      plan2.loc[(plan2["if_new"] == True)&(plan2["num"]==1), "id":"ratio"].shape[0],
      plan2.loc[(plan2["if_new"] == True)&(plan2["num"]==1)&(plan2["ratio"]>0.5), "id":"ratio"].shape[0],
      plan2.loc[(plan2["if_new"] == True)&(plan2["num"]>1), "id":"ratio"].shape[0],
      plan2.loc[(plan2["if_new"] == True)&(plan2["num"]>1)&(plan2["ratio"]>0.5), "id":"ratio"].shape[0])

print()
print("plan3", plan3.loc[plan3["if_new"] == False, "id":"ratio"].shape[0],
      plan3.loc[plan3["if_new"] == False, "id":"ratio"][plan3.loc[plan3["if_new"] == False, "id":"ratio"]["recently_joined"]==False].shape[0],
      plan3.loc[plan3["if_new"] == False, "id":"ratio"].loc[plan3.loc[plan3["if_new"] == False, "id":"ratio"]["ratio"]>0.5].shape[0],
      plan3.loc[(plan3["if_new"] == True)&(plan3["num"]==1), "id":"ratio"].shape[0],
      plan3.loc[(plan3["if_new"] == True)&(plan3["num"]==1)&(plan3["ratio"]>0.5), "id":"ratio"].shape[0],
      plan3.loc[(plan3["if_new"] == True)&(plan3["num"]>1), "id":"ratio"].shape[0],
      plan3.loc[(plan3["if_new"] == True)&(plan3["num"]>1)&(plan3["ratio"]>0.5), "id":"ratio"].shape[0])
print()
print("plan4", plan4.loc[plan4["if_new"] == False, "id":"ratio"].shape[0],
      plan4.loc[plan4["if_new"] == False, "id":"ratio"][plan4.loc[plan4["if_new"] == False, "id":"ratio"]["recently_joined"]==False].shape[0],
      plan4.loc[plan4["if_new"] == False, "id":"ratio"].loc[plan4.loc[plan4["if_new"] == False, "id":"ratio"]["ratio"]>0.5].shape[0],
      plan4.loc[(plan4["if_new"] == True)&(plan4["num"]==1), "id":"ratio"].shape[0],
      plan4.loc[(plan4["if_new"] == True)&(plan4["num"]==1)&(plan4["ratio"]>0.5), "id":"ratio"].shape[0],
      plan4.loc[(plan4["if_new"] == True)&(plan4["num"]>1), "id":"ratio"].shape[0],
      plan4.loc[(plan4["if_new"] == True)&(plan4["num"]>1)&(plan4["ratio"]>0.5), "id":"ratio"].shape[0])
print()

'''

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
