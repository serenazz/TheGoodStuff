import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from pandas import HDFStore
store=HDFStore('storage1.h5')
df1=store['df_final']
df1=df1.drop("first",1)
df1=df1.drop("last",1)
df1=df1.drop("recently_joined",1)
df1=df1.drop("if_new",1)

follow=[]
with open("pushed.csv") as file:
    i=file.readline()
    i=i.split(",")
    for m in i:
        follow.append(m)

bought=pd.read_csv("bought_24Hr.csv")
bought=bought["id"].tolist()
def label_plan(row,plan):
    if str(row["id"]) in plan:
        return 1
    else:
        return 0
df1["follow"]= df1.apply(lambda row:label_plan(row,follow), axis=1)
df1=df1.loc[(df1["canceled"]==0)&(df1["follow"]==1)&(df1["plan"]==4),:]
df1=df1.drop("canceled",1)
df1=df1.drop("follow",1)

def check_bought(row):
    if row["bought"]>0:
        return 1
    else:
        return 0
df1["if_bought"]= df1.apply(lambda row:check_bought(row), axis=1)


def check_price_sen(row):
    if (row["ratio"]>0.5) or (row["c_ratio"]>0.5):
        return 1
    else:
        return 0
df1["price_sen"]= df1.apply(lambda row: check_price_sen(row), axis=1)



X=df1.loc[:,("num","first_order_interval","last_order_interval","price_sen")]
y=df1.loc[:,["if_bought"]]

#data exploration
print(df1.groupby("clicked").mean())

#regression
y = np.ravel(y)
model=LogisticRegression(class_weight="balanced")
model=model.fit(X,y)
print(model.score(X,y))
print(y.mean())
print(pd.DataFrame(list(zip(X.columns, np.transpose(model.coef_)))))

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=0)
model2 = LogisticRegression()
model2=model2.fit(X_train, y_train)
predicted=model2.predict(X_test)
probs=model2.predict_proba(X_test)
print(predicted)
print(probs)
# generate evaluation metrics
print ("accuracy: ",metrics.accuracy_score(y_test, predicted))
print ("roc_auc: ",metrics.roc_auc_score(y_test, probs[:, 1]))
scores = cross_val_score(LogisticRegression(), X, y, scoring='accuracy', cv=10)
print (scores)
print(scores.mean())
print("我预测",model.predict(np.array([1,1,20,1])))


#=======
modelTree=DecisionTreeClassifier(class_weight="balanced")
modelTree.fit(X,y)
print(modelTree)
# make predictions
expected_T = y
predicted_T = modelTree.predict(X)
probs_T=modelTree.predict_proba(X_test)
# summarize the fit of the model
'''
print(metrics.classification_report(expected_T, predicted_T))
print(metrics.confusion_matrix(expected_T, predicted_T))
'''
#print ("accuracy: ",metrics.accuracy_score(y_test, predicted_T))
print ("roc_auc: ",metrics.roc_auc_score(y_test, probs_T[:, 1]))
scores = cross_val_score(DecisionTreeClassifier(), X, y, scoring='accuracy', cv=10)
print (scores)
print(scores.mean())
print("我预测",modelTree.predict(np.array([1,1,20,0])))
print(predicted_T)
print(probs_T)