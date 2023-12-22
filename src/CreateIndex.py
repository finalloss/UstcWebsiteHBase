from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

index_name = "titleindex1"

mappings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "ik_max_word"
                },
                "default_search": {
                    "type": "ik_smart"
                }
            }
        }
    },
    "mappings": {
        "_doc":{
            "properties": {
                "link":{
                    "type": "keyword",
                    },
                "title":{
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart"
                },
                "time":{
                    "type": "date",
                    "format":"yyyy/MM/dd"
                }
            }
        }   
    }
}
es.indices.create(index=index_name,body=mappings)
