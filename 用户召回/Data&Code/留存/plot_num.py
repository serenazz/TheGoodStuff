import pandas as pd
from matplotlib import pyplot as plt
import datetime



df=pd.read_csv("recent_lost.csv")
df=df.dropna()
df['first']=pd.to_datetime(df['first'],format ="%Y-%m-%d")
df['last']=pd.to_datetime(df['last'],format ="%Y-%m-%d")
df['first_order_interval'] = (pd.Series(datetime.datetime.now(), index=df.index) - df['first']).astype('timedelta64[D]').astype('int')
df['last_order_interval']=(pd.Series(datetime.datetime.now(), index=df.index) - df['last']).astype('timedelta64[D]').astype('int')
df=df.sort_values(by="last_order_interval")
df=df[df.first_order_interval>90]
#df2=df[df.last_order_interval>=30]

'''
df2=df[df.num>10].sort_values(by="num")
df2=df2[df2.num<100].sort_values(by="num")
'''
print(df["num"].value_counts(normalize=True))
df["num"].plot.hist(alpha=0.5)
plt.show()