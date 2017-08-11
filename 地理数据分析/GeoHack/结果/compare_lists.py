import pandas as pd
import collections

#load zxs addresses and convert all zxs addresses to list: all_address
df=pd.read_csv("all_address.csv")
all_address=df["address"].tolist()

#load region data and convert to a list: all_chaoyang_address
df_chaoyang=pd.read_csv("haidian_addresses.csv")
all_chaoyang_addresss=df_chaoyang["name"].tolist()

#get list of distinct community in the region and convert to dataframe:cleaned
frequency=collections.Counter(item[:4] for item in all_chaoyang_addresss).items()
list_chaoyang=[]
for i, value in frequency:
    list_chaoyang.append([i,value])
cleaned=pd.DataFrame(list_chaoyang,columns=["name","repeat"])
print(cleaned)

#check for specific community, how many zxs are in there
def find_occurance(row):
    to_search=row["name"]
    cnt=0
    for i in all_address:
        if to_search in i:
            cnt+=1
    return cnt
cleaned["occurance"]=cleaned.apply(lambda row: find_occurance(row), axis=1)
print(cleaned["name"].shape[0])
#number of communities with zxs
print(cleaned.loc[cleaned["occurance"]>0].shape[0])
#number of communities without zxs
print(cleaned.loc[cleaned["occurance"]==0].shape[0])
print(cleaned.loc[cleaned["occurance"]>9])
