from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import ElasticsearchException
import csv
import uuid
import configurations as conf
import geojson
import json
import sys



# es=Elasticsearch([conf.host_addr+':'+conf.host_port],http_auth=(conf.elastic_username, conf.elastic_password))
es = Elasticsearch(['localhost:9200'])

print(es.indices.delete(index=conf.index_name, ignore=[400, 404]))

response = es.indices.create(
    index=conf.index_name,
    body=conf.mapping,
    ignore=400 # ignore 400 already exists code
)
print('response:', response)

url = 'C:\\Users\\Dell\\Documents\\GIS DataBase\\processed\\popmap15adj_gt_3.geojson'
# url = conf.file_path

# with open(url) as f:
#     data = geojson.load(f)


iterator = 0
batch = 0
tmp_array = []

def insert_batch_in_elasticsearch(batch):
  actions = []
  # batch = batch[5:]
  for b in batch:
    b = b.replace(',\n', '')
    json_tmp = json.loads(b)
    doc = {
        "fid": json_tmp['properties']['fid'],
        'x': round(json_tmp['geometry']['coordinates'][0],4),
        'y': round(json_tmp['geometry']['coordinates'][1],4),
        'pop': json_tmp['properties']['VALUE'],
        'location':
          {
            "lat": str(round(json_tmp['geometry']['coordinates'][1],4)),
            "lon": str(round(json_tmp['geometry']['coordinates'][0],4))
          }
    }
    # print(doc)
    action = [{"_source": doc}]
    actions.append(action[0])

  try:
    response = helpers.bulk(es, actions, index=conf.index_name)
    print("\nRESPONSE:", response)
  except ElasticsearchException as e:
    print("\nERROR:", e)



with open(url) as infile:
  # zero_iterator = 0
  for line in infile:
    # print(line)
    if ('VALUE' in line and json.loads(line.replace(',\n',''))["properties"]["VALUE"] >= conf.pop_threshhold):
    # if ('VALUE' in line and json.loads(line.replace(',\n', ''))["properties"]["VALUE"] == 0.0):
      # zero_iterator = zero_iterator + 1
      # print(zero_iterator)
      iterator = iterator + 1
      tmp_array.append(line)
      if iterator==conf.batch_size:
        batch = batch+1
        # print(str(batch)+'th batch processed..')
        insert_batch_in_elasticsearch(tmp_array)
        iterator = 0
        tmp_array = []

