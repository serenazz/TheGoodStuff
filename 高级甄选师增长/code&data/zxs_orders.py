import pandas as pd
import datetime
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv


df=pd.read_csv("zxs_orders.csv")

print(df.shape)
df=df.dropna(axis=0, how ="any")
print(df.isnull().sum())
print(df.shape)

df=df.sort_values(by="orders")
df1=df[df.orders<30]
#df1=df1[df1.orders<150]

df1=df1[np.abs(df.orders-df.orders.mean())<=(3*df.orders.std())]
print(df1.shape)
#df1=df1[:-50]

kmeans=KMeans(n_clusters=4).fit(df1.loc[:,["days","orders"]])
labels=kmeans.labels_
centroids = kmeans.cluster_centers_

colors=['red','green', 'blue','yellow',"black"]
for i in range(4):
    ds=df1.as_matrix()[np.where(labels==i)]
    plt.plot(ds[:,2], ds[:,1],'o', color=colors[i])

#plot original
# plt.plot(df1.loc[:,["days"]],df1.loc[:,["orders"]],"o")
plt.show()