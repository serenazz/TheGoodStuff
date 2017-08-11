# -*- coding:utf-8 -*-
import urllib
import http
import json
import socket
import os
import base64


## An object of this class can be used to return the longitute and latitute of
## the address(es). One can call the getLocation function to get the value for
## each address, or use batchFinder to transform addresses in a file to
## corresponding values. Note the format of the file shall be further clarified,
## and the code has to be modified accordingly.
#MbHwxkEeQbRSGIOXO9Gsgdtnk0b4G4B4
class POIFinder:
    def __init__(self, key='MbHwxkEeQbRSGIOXO9Gsgdtnk0b4G4B4'):  # ''
        self.host = 'http://api.map.baidu.com'
        self.path = '/place/v2/search?'
        # self.param={'address':None,'output':'json','ak':key}#,'location':None,'city':None}
        self.param = {'query': None, 'scope': 2, 'coord_type': 3, 'page_size': 20, 'output': 'json', 'ak': key,
                      'location': None, 'radius': None, 'page_num': None}
        # Following parameters is for transfering coordinates from GPS to Baidu
        self.transfer_host = 'http://api.map.baidu.com'
        self.transfer_path = '/ag/coord/convert/?'
        self.transfer_param = {'from': 0, 'to': 4, 'x': None, 'y': None}  # x is longitude, y is latitude

    def getPOIinfo(self, lat, long, radius, query_type):
        # Return the POI results of a certain location in a list. Note that sometimes there's no detail information for
        # a certain record in the results. In that case, the record is a list of length 2. Else it's a list of length 4
        num_pages = 1
        page = 0
        result = []
        while page < num_pages:
            rlt = self.request_form(lat, long, radius, query_type, page_num=page)
            list_poi = rlt['results'] if rlt is not None else []
            for poi_point in list_poi:
                result.append([poi_point["name"], poi_point["uid"]] + ([poi_point["detail_info"].get("tag", ""),
                                                                        poi_point["detail_info"].get("type", "")] if
                                                                       poi_point["detail"] else []))
            page += 1
            num_pages = (rlt['total'] - 1) / 20 + 1 if rlt is not None else 0
        return result

    def request_form(self, lat, long, radius, query_type, page_num):
        self.param['query'] = query_type
        self.param['location'] = str(lat) + "," + str(long)
        self.param['radius'] = radius
        self.param['page_num'] = page_num
        valueerror_times = 0  # For unknown reason, there can be value error during json.loads(), which does not
        # automatically disappear when we repeat the request. Therefore we introduce the value error time threshold to
        # terminate the while loop
        while True:
            try:
                r = urllib.request.urlopen(self.host + self.path + urllib.urlencode(self.param), timeout=60)
                rlt = json.loads(r.read())
                if rlt['status'] == 0:
                    return rlt
                else:
                    print( rlt['message'])
                    if rlt['message'] == u"天配额超限，限制访问":
                        raise TypeError(u"天配额超限，限制访问。请明天0点后再使用")
                    return None
            except ValueError:
                print ('No response from Baidu for value {}, {} with radius {}'.format(lat, long, radius) + ', try again')
                valueerror_times += 1
                if valueerror_times <= 5:  # If we meet more than 5 times ValueError, end this request and return None
                    continue
                else:
                    return None
            except socket.timeout:
                print ('Timeout from Baidu for value {}, {} with radius {}'.format(lat, long, radius) + ', try again')
                continue
            except http.client.BadStatusLine:
                print ("Unknown error, try again")
                continue
            except urllib.request.HTTPError:
                print ("Unkonwn error, try again")
                continue

if __name__ == '__main__':
    query_types = ["美食", "酒店", "购物", "生活服务", "旅游景点", "休闲娱乐", "运动健身", "教育培训", "文化传媒", "医疗",
                   "汽车服务", "交通设施", "金融", "房地产", "公司企业", "政府机关"]
    pf = POIFinder()
    target_label = "宿舍$商铺$生活服务"
    place_list = [(30.64260676, 104.075023), (30.70587238, 104.107904)]
    for i, place in enumerate(place_list):
        results = pf.getPOIinfo(place[0], place[1], 200, target_label)
        print ("Result for place #{}, {} items returned".format(i, len(results)))
        for result in results:
            print( ",".join(result))

'''
if __name__ == '__main__':
    file=open(r"3mzxsaddress.json",encoding='utf-8')
    data=[]
    newData=[]
    for line in file:
        data.append(json.loads(line[:-2]))
    for dic in data:
        address=dic['地址']
        lat,lng=getlnglat(address)
        dic['lat']=lat
        dic['lng']=lng
        newData.append(dic)
    for dic in newData:
        __jsonDump("HuaiRou",dic)
'''