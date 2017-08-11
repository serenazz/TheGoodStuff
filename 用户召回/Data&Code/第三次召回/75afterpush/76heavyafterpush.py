from pandas import HDFStore
import pandas as pd

store=HDFStore('july.h5')
df=store["df_76_all"]

#获取模板消息人群#
normal=pd.read_csv("76_normal.csv")
value=pd.read_csv("76_value.csv")


for i in (normal,value):
    print(i.shape[0])


#normal["userid"].to_frame().to_csv("76pushed.csv",sep=',',index=False, line_terminator=',')
#value["userid"].to_frame().to_csv("76value.csv",sep=',',index=False, line_terminator=',')


def label_plan(row):
    if row["id"] in normal["userid"].tolist():
        return 1
    elif row["id"] in value["userid"].tolist():
        return 2
    else:
        0
#加入分组标签
df["plan"]=df.apply(lambda row:label_plan(row), axis=1)
print(df["plan"].value_counts())


#获取点击/购买名单
clicked=pd.read_csv("7576clicked.csv", delimiter="\n")
bought=pd.read_csv("76D1_bought.csv")
bought=bought["id"].tolist()
clicked=clicked["id"].tolist()
for index in range(len(bought)):
    bought[index]=int(bought[index])
for index in range(len(clicked)):
    clicked[index]=int(clicked[index])
c=0
for i in bought:
    if i in clicked:
        continue
    else:
        c+=1
print("c",c)

#添加各行为字段
def label_action(row,action):
    count=action.count(row["id"])
    return count
df["clicked"]=df.apply(lambda row:label_action(row,clicked), axis=1)
df["bought"]=df.apply(lambda row:label_action(row,bought), axis=1)

print("normal:3489","value: 1353")

print(df.loc[(df["bought"]>0)]["plan"].value_counts())
print(df.loc[(df["clicked"]>0)]["plan"].value_counts())