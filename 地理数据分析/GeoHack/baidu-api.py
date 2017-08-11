import urllib3
import requests
import json
import http

http=urllib3.PoolManager()

'''
def divide_city():
    #海淀
    location=[40.098998,116.187777,39.905167,116.362767]
    #朝阳
    #location=[40.039863,116.454143,39.85226,116.576995]
    # location 为北京
    #location=[40.3151980000, 115.7020240000, 39.5770810000, 117.0335290000]
    dif = [location[0] - location[2], location[3] - location[1]]
    b = [x / 100.0 + location[2] for x in range(int(dif[0] * 100))]
    c = [x / 100.0 + location[1] for x in range(int(dif[1] * 100))]
    cord = [[x, y] for x in b for y in c]
    return cord
'''
def getlnglat(address):
    """根据传入地名参数获取经纬度"""
    url = 'http://api.map.baidu.com/geocoder/v2/'
    """根据传入地址获得poi"""
    #url='http://api.map.baidu.com/place/v2/search'
    output = 'json'
    ak = "kIfABCYd04L0SDeWOv9189aHYtvefrAv"##'MbHwxkEeQbRSGIOXO9Gsgdtnk0b4G4B4'"location":"116.3436956,39.9197507","filter":None,"region":"北京",    """type:house"""
    #fields={"query":"小区","bounds":"{},{},{},{}".format(x,y,x+0.01,y+0.01),"output":output,"ak":ak,"scope":2}
    fields={"address":address,"output":output,"ak":ak,}
    #radius of beijing 72270000 m, center:"location":"39.9042,116.4074"
    req = http.request_encode_url('GET',url,fields)
    res = req.data.decode()
    temp = json.loads(res)
    '''
    if temp["status"]!=0:
        print("message",temp["message"])
        return 0
    else:
        print(temp)
        l=temp["results"]
        data=[]
        for line in l:
            data.append(line)
        return data
    '''
    lat=temp['result']['location']['lat']
    lng=temp['result']['location']['lng']
    return lat,lng

if __name__ == '__main__':
    '''
    data={}
    data["result"]=[]

    cord_groups=divide_city()
    #cord_groups=[39.85226, 116.454143], [39.85226, 116.474143],
    print(cord_groups)
    print(len(cord_groups))
    for cord in cord_groups:
        x=cord[0]
        y=cord[1]
        result=getlnglat(x,y)
        if result==0:
            break
        else:
            for line in result:
                data["result"].append(line)
    with open("json_output.txt","w",encoding='utf8') as f:
        json.dump(data,f,ensure_ascii=False)
    #getlnglat("北京市朝阳区望京花园东区")

    #换zxs经纬度
    '''
    file=open(r"haidian_group1.json",encoding='utf-8')
    data=json.load(file)

    for line in data:
        try:
            line["lat"],line["long"]=getlnglat(line["address"])
        except ValueError:
            print ('No response from Baidu for value {}, {} with radius {}')
            #.format(lat, long, radius) + ', try again')
            #valueerror_times += 1
            #if valueerror_times <= 5:  # If we meet more than 5 times ValueError, end this request and return None
                #continue
            #else:
                #return None
        #except socket.timeout:
            #print ('Timeout from Baidu for value {}, {} with radius {}'.format(lat, long, radius) + ', try again')
            #continue
        #except http.client.BadStatusLine:
            #print ("HTTP, try again")
            #continue
        except:
            print ("Unkonwn error, try again")
            continue

        print("{'lng':",line["long"],",","'lat':",line["lat"],",","'count':",line["orders"],"},")

    #json.dump("dumped.txt",final_data,sort_keys=True,indent=2)
    print("finished!")
