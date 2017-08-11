import pandas as pd
from matplotlib import pyplot as plt

df=pd.read_csv("after_march_frequency.csv")

pd.to_numeric(df.days_range)
pd.to_numeric(df.orders)
pd.to_numeric(df.frequency)
df=df.loc[df["zxs"]==38617]


df=df.loc[(df["frequency"]>0)&(df["days_range"]>30)]
groups=pd.cut(df.frequency,20)
print(groups.value_counts())
print(df.frequency.describe())
print(df.loc[df["orders"]>1].shape[0])


print(df.loc[df["frequency"]>9].shape[0])
print(df.shape[0])

#单量总览
groups=pd.cut(df.orders,20)
print(groups.value_counts())
print(df.orders.describe())
print()

df.frequency.plot.hist(alpha=0.5,range=[0,40],bins=200)
plt.xlabel("购买间隔时间")
plt.ylabel=("符合条件人数")
plt.show()

#75%上的用户平均1周买一次