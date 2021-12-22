import json
from elasticsearch import Elasticsearch

# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es = Elasticsearch()


with open('decor_data.json', encoding='utf-8') as f:
    json_docs = json.load(f)
    num = 1
    for json_doc in json_docs:
            doc = json_doc
            res = es.index(index="leroymerlindecor", doc_type='_doc', document=doc, id=str(num))
            num+=1