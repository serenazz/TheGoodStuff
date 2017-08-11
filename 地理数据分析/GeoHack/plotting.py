import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import json
import folium


map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0, lat_0=0, lon_0=-130)
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'gray')
map.drawmapboundary()
map.readshapefile('/Users/zmn/Documents/CHN_adm_shp/CHN_adm2', 'CHN_adm2')



if __name__ == '__main__':
    file=open(r"Vupdated.json",encoding='utf-8')
    data=[]
    data=json.load(file)
    '''
    map_osm= folium.Map(location=[45.5236, -122.6750]) #输入坐标
    map_osm.create_map(path='osm.html')
    '''

    for line in data:
        x,y=map(line["long"],line["lat"])
        print(x,y)
        map.plot(x, y, marker='o',color="green")

    plt.show()
