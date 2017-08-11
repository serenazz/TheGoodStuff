import pandas as pd
import datetime
'''
#without filtering out weekday/weekend
df=pd.read_csv("fav_time_without_pro.csv")
df1=df.groupby("id").size().to_frame().rename(columns={0:"cnt"})
df1["id"]=df1.index
df2=pd.merge(df,df1,how="left",on="id")
df2["cnt"]=1/df2["cnt"]
print(df2.groupby("hour")["cnt"].sum())
'''

df_week=pd.read_csv("before_march.csv")
# df_week=pd.read_csv("apr_may_without_prodays_overall.csv")
#df_week=df_week[df_week["dow"]==2]

#df_weekend=pd.read_csv("fav_time_without_pro_weekend.csv")
df_week["time"]=pd.to_datetime(df_week['time'],format ="%Y-%m-%d %H")
df_week["hour"]=df_week["time"].dt.hour
df_week_1=df_week.groupby(["id","hour"]).size().to_frame().rename(columns={0:"cnt"}).reset_index()
inx=df_week_1.groupby(["id"])["cnt"].transform(max)==df_week_1["cnt"]
df_week_2=df_week_1[inx]


df1=df_week_2.groupby("id").size().to_frame().rename(columns={0:"cnt_occ"})
df1["id"]=df1.index
print(df1.head(100))
df2=pd.merge(df_week_2,df1,how="left",on="id")
df2["cnt_occ"]=1/df2["cnt_occ"]
#print(df2.head(100))
#df2=(df2-df2.min())/(df2.max()-df2.min())
print(df2.groupby("hour")["cnt_occ"].sum())
