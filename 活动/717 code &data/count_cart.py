import pandas as pd

df=pd.read_csv("717cartdata.csv")
print(df.head(10))

dfc=df.groupby("orderid")["merid"].nunique().to_frame().reset_index()
dfc=dfc.loc[dfc["merid"]>1]
print(dfc.shape[0])
print(dfc.head(10))