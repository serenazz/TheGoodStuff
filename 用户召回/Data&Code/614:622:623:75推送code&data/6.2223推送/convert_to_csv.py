import pandas as pd
import csv
#
list=pd.read_csv("623_guanzhu.csv",delimiter="\n")
list=list["id"].tolist()
#  生成推送成功的名单,以便sql查询
with open("623_guanzhu.csv","w") as f:
    spamwriter = csv.writer(f, delimiter=',')
    spamwriter.writerow(list)



