import pandas as pd
#import pysql
df = pd.read_csv('april_user.csv')
# 暂时分析2017 数据
df['time']=pd.to_datetime(df['time'],format ="%Y-%m-%d %H")
df=df[df.time>='2016-12-31 23']
value_distribution = df.order.value_counts()
value_distribution=value_distribution.to_frame().reset_index()
value_distribution=value_distribution.rename(columns={'index':'nums','order':'records'})
value_distribution['weight']= value_distribution['records']*value_distribution['nums']
print(value_distribution)
avg=value_distribution.weight.sum()/value_distribution.records.sum()
print(avg)


#一个用户每小时平均下单1.385个, 去掉甄选师后,可能会更小.