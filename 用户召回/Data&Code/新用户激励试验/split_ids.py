import pandas as pd

df=pd.read_csv("722new.csv")
print()
df1=df.loc[(df["product_id"]==314)]

delete_date=df1.id.tolist()
df2=df[~df["id"].isin(delete_date)]
print(df2["product"].value_counts())
print(df.id.nunique())
print(df1.id.nunique())
df2=df2.loc[df2["coupon"]==0]

listn=df2.id.unique().tolist()
print(len(listn))
print(df2.id.nunique())

plan1=df2.sample(frac=0.333)
plan2=df2.drop(plan1.index).sample(frac=0.5)
plan3=df2.drop(plan1.index).drop(plan2.index).sample(frac=1)
lplan1=plan1["id"].tolist()
lplan2=plan2["id"].tolist()
lplan3=plan3["id"].tolist()
print(len(lplan1))
print(len(lplan2))
print(len(lplan3))
plan1["id"].to_frame().to_csv("722coupon",sep=',',index=False, line_terminator=',')
plan2["id"].to_frame().to_csv("722kiwi",sep=',',index=False, line_terminator=',')
plan3["id"].to_frame().to_csv("722control",sep=',',index=False, line_terminator=',')
#df2=df.loc[(df["product_id"]!=634)&(df["coupon"]==0)]
#print(df1.id.nunique())
#print(df.id.nunique())