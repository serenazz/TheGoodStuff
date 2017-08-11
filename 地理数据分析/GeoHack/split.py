import pandas as pd

df=pd.read_csv("haidian_user.csv")

plan1=df.sample(frac=0.2)
plan2=df.drop(plan1.index).sample(frac=0.25)
plan3=df.drop(plan1.index).drop(plan2.index).sample(frac=0.333333333)
plan4=df.drop(plan1.index).drop(plan2.index).drop(plan3.index).sample(frac=0.5)
plan5=df.drop(plan1.index).drop(plan2.index).drop(plan3.index).drop(plan4.index).sample(frac=1)


for i in (plan1,plan2,plan3,plan4,plan5):
    print(i.shape[0])
plan1.to_csv("plan1.csv",index=False)
plan2.to_csv("plan2.csv",index=False)
plan3.to_csv("plan3.csv",index=False)
plan4.to_csv("plan4.csv",index=False)
plan5.to_csv("plan5.csv",index=False)