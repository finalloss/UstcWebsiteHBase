from elasticsearch import Elasticsearch
import happybase
from CreateIndex import index_name

def transform_data(hbase_conn,es):
    table = hbase_conn.table("resource")
    for key, data in table.scan(columns=[b'info:title', b'info:link', b'info:date']):
        doc = {
        'title': data.get(b'info:title').decode('utf-8'),
        'link': data.get(b'info:link').decode('utf-8')
    }

    # Add 'date' to document only if it exists
        if b'info:date' in data:
            if data[b'info:date'].decode('utf-8'):
                print(data[b'info:date'].decode('utf-8'))
                doc['date'] = data[b'info:date'].decode('utf-8')

        es.index(index=index_name,doc_type='_doc',id=key.decode('utf-8'),body=doc)


hbase_conn = happybase.Connection(port=9090)
es = Elasticsearch(['http://localhost:9200'])
transform_data(hbase_conn,es)
