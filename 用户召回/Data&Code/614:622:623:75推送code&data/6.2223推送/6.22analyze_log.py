import pandas as pd
from pandas import HDFStore
from datetime import datetime

store = HDFStore('storage1.h5')
df1= store["pushed_browse6_22"]
all=store["622pushed"]
print(df1.tail())
df1["sub1"],df1["sub2"]=df1["suburl"].str.split("&",1).str




fit_user=[]
prev=-1
count_url=0
for index, row in df1.iterrows():
    if prev<0:
        prev=index
        continue
    else:
        uid=df1.iloc[prev]["userid"]
        print(uid)
        if df1.iloc[prev]["url"]=="商品详情" and df1.iloc[prev]["sub1"]=="id=534":
            count_url+=1
            print(uid)
            print(df1.iloc[index]["userid"])
            print(df1.iloc[prev]["time"],df1.iloc[prev]["userid"],df1.iloc[prev]["url"],df1.iloc[prev]["suburl"])
            print(df1.iloc[index]["time"],df1.iloc[index]["userid"],df1.iloc[index]["url"],df1.iloc[index]["suburl"])
        prev=index
'''
            if df1.iloc[index]["url"]=="首页" and df1.iloc[index]["userid"]==uid:
                fit_user.append(uid)
            elif df1.iloc[index]["userid"]==uid:
                print(df1.iloc[index]["url"],df1.iloc[index]["suburl"])

    print("==========")

print(len(fit_user))
print(count_url)
'''
