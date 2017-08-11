import pandas as pd
import numpy as np

df=pd.read_csv("729user.csv")

'''
#分组
controlled=df.sample(frac=0.5)
plan1=df.drop(controlled.index).sample(frac=0.25)
plan2=df.drop(controlled.index).drop(plan1.index).sample(frac=0.333333)
plan3=df.drop(controlled.index).drop(plan1.index).drop(plan2.index).sample(frac=0.5)
plan4=df.drop(controlled.index).drop(plan1.index).drop(plan2.index).drop(plan3.index).sample(frac=1)


plan1["id"].to_frame().to_csv("plan1",sep=',',index=False, line_terminator=',')
plan2["id"].to_frame().to_csv("plan2",sep=',',index=False, line_terminator=',')
plan3["id"].to_frame().to_csv("plan3",sep=',',index=False, line_terminator=',')
plan4["id"].to_frame().to_csv("plan4",sep=',',index=False, line_terminator=',')
controlled["id"].to_frame().to_csv("controlled",sep=',',index=False, line_terminator=',')

print(plan1.shape[0])
print(plan2.shape[0])
print(plan3.shape[0])
print(plan4.shape[0])
print(controlled.shape[0])
'''
'''
7614
7614
7614
7613
30456
'''
