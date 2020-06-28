import json
import geojson

# url = 'C:\\Users\\Dell\\Documents\\GIS DataBase\\processed\\extent2.geojson'
url = 'C:\\Users\\Dell\\Documents\\GIS DataBase\\processed\\popmap15adj_vector_points_gt_5_geojson.geojson'

with open(url) as f:
    data = geojson.load(f)

for d in data['features']:
    print('x : '+ str(d['geometry']['coordinates'][0]) + ' y : ' + str(d['geometry']['coordinates'][1]) + ' VAL : ' + str(d['properties']['VALUE']))
    # print(d['features'][0]['geometry'])
# print(data['features'][0]['geometry'])
