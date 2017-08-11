import urllib3
import json

http=urllib3.PoolManager()


def getpoi():
    """根据传入地名参数获取经纬度"""
    """根据传入地址获得poi"""
    url='http://api.map.baidu.com/place/v2/detail'
    output = 'json'
    ak = 'MbHwxkEeQbRSGIOXO9Gsgdtnk0b4G4B4'#"kIfABCYd04L0SDeWOv9189aHYtvefrAv""location":"116.3436956,39.9197507","filter":None,"region":"北京",    """type:house"""
    fields={"uid":"5a8fb739999a70a54207c130","output":output,"ak":ak,"scope":"2"}
    req = http.request_encode_url('GET',url,fields)
    res = req.data.decode()
    temp = json.loads(res)
    print(temp)
    return temp
if __name__ == '__main__':
    getpoi()
    another="1840d4e0115f610e9d95def1"
    '''
    file=open(r"target.json",encoding='utf-8')
    data=json.load(file)

    for line in data:
        try:
            line["lat"],line["long"]=getpoi(line["uid"])
        except ValueError:
            print ('No response from Baidu for value {}, {} with radius {}')
        except:
            print ("Unkonwn error, try again")
            continue
    #json.dump("target_poi.txt",data,sort_keys=True,indent=2)
    print("finished!")
    '''