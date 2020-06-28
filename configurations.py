# elasticsearch configurations
host_addr = '172.16.1.65'
host_port = '9202'
elastic_username = 'elastic'
elastic_password = 'elastic123'
index_name = 'popmap15adj_gt_3'
batch_size = 10000
file_path = '/data/processed/popmap15adj_gt_3.geojson'
pop_threshhold = 3

buffer_distance = 0.008
# elasticsearch mapping for the rollout index
mapping = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "fid": {
                "type": "long"
            },
            "x":{
                "type":"long"
            },
            "y":{
                "type":"long"
            },
            "location" : {
              "type" : "geo_point"
            },
            "pop":{
                "type":"long"
            }
        }
    }
}

query_body = {
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "District": "BAHAWALNAGAR"
          }
        }
      ]
    }
  }
}