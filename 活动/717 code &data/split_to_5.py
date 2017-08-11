import pandas as pd
import numpy as np

df=pd.read_csv("717weixin.csv")

'''
#分组
plan1=df.sample(frac=0.2)
plan2=df.drop(plan1.index).sample(frac=0.25)
plan3=df.drop(plan1.index).drop(plan2.index).sample(frac=0.333333)
plan4=df.drop(plan1.index).drop(plan2.index).drop(plan3.index).sample(frac=0.5)
plan5=df.drop(plan1.index).drop(plan2.index).drop(plan3.index).drop(plan4.index).sample(frac=1)


plan1["id"].to_frame().to_csv("plan1",sep=',',index=False, line_terminator=',')
plan2["id"].to_frame().to_csv("plan2",sep=',',index=False, line_terminator=',')
plan3["id"].to_frame().to_csv("plan3",sep=',',index=False, line_terminator=',')
plan4["id"].to_frame().to_csv("plan4",sep=',',index=False, line_terminator=',')
plan4["id"].to_frame().to_csv("plan5",sep=',',index=False, line_terminator=',')
'''
df["id"].to_frame().to_csv("allnum.csv",sep=',',index=False, line_terminator=',')