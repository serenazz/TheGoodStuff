import csv
import pandas as pd
from pandas import HDFStore
store=HDFStore('july.h5')
df=store["df_75_all"]
print(df.head(5))


with open("broken.csv") as f:
    spamreader = csv.reader(f, delimiter=',')
    broken=list(spamreader)[0]
print("后发:", len(broken))
for index in range(len(broken)):
    broken[index]=int(broken[index])

#获取模板消息人群#
real_normal=pd.read_csv("75_real_normal.csv")
real_single1=pd.read_csv("75_real_single1.csv")
real_single2=pd.read_csv("75_real_single2.csv")


for i in (real_normal,real_single1,real_single2):
    print(i.shape[0])

#创建模板消息+券的正确人群#
def if_in(row,list):
    if row["userid"] in list:
        return 1
    else:
        return 0

real_normal["if_keep"]= real_normal.apply(lambda row: if_in(row,broken), axis=1)
filter_normal=real_normal.loc[real_normal["if_keep"]==0]
real_single1["if_keep"]= real_single1.apply(lambda row: if_in(row,broken), axis=1)
filter_single1=real_single1.loc[real_single1["if_keep"]==0]
real_single2["if_keep"]= real_single2.apply(lambda row: if_in(row,broken), axis=1)
filter_single2=real_single2.loc[real_single2["if_keep"]==0]

print("真实")
for i in (filter_normal,filter_single1,filter_single2):
    print(i.shape[0])

def label_plan(row):
    if row["id"] in real_normal["userid"].tolist():
        return "normal"
    elif row["id"] in real_single1["userid"].tolist():
        return "single1"
    elif row["id"] in real_single2["userid"].tolist():
        return "single2"
    else:
        0
#加入分组标签
df["plan"]=df.apply(lambda row:label_plan(row), axis=1)
print(df["plan"].value_counts())
store.put('df_75_afterpush',df,format="table")
store.close()
#generat pushed list
#real_normal["userid"].to_frame().to_csv("75pushed.csv",sep=',',index=False, line_terminator=',')
#real_single1["userid"].to_frame().to_csv("1.csv",sep=',',index=False, line_terminator=',')
#real_single2["userid"].to_frame().to_csv("2.csv",sep=',',index=False, line_terminator=',')


#1379
'''
with open("75correctnormal.csv") as f:
    spamreader = csv.reader(f, delimiter=',')
    normal_prev=list(spamreader)[0]
print("历史已经推送:", len(normal_prev))

'''
