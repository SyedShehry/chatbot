from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from data import get_data
from open_ai import chat_bot

es_client = Elasticsearch(
    cloud_id = "9fce15780618432c8f33529d634d1fce:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmMzQ2OTkyNzc2MGQ0MzE3YmFkNTBkOWIyNGMyMDEwMCQ2MDBkZDI1MjMzNDc0ZGM3OTI2NzkxNjhkM2M2ZGM5YQ==",
    basic_auth = ("elastic", "OhGKuj5af4UGo6p9txKgC76B"),
)

def create_index(index_name):
    es_client.indices.create(
        index = index_name,
        mappings={
            "properties": {
                "id": {
                    "type": "text",
                },
                "data": {
                    "type": "text",
                },
                "embeddings": {
                    "type": "dense_vector",
                    "dims": 768, 
                }
            }
        }
    )

embedder = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

def index_content(data, id, index_name):
    embeddings = embedder.encode(data)
    data = {
        "id": id,
        "data": data,
        "embeddings": embeddings
    }
    es_client.index(
        index= index_name,
        document= data
    )

# web_url = "https://en.wikipedia.org/wiki/Punjab,_Pakistan"
# data = get_data(url=web_url)
# id = 0

# for chunks in data:
#     index_content(id=id, data=chunks, index_name="wikipedia_data")
#     print(f'data for id={id} is indexed in elastic search')
#     id += 1

# create_index("wikipedia-data")

def query_data(query, index_name):
    embeddings = embedder.encode(query)
    results = es_client.search(
        index=index_name,
        size = 2,
        from_ = 0,
        source = ['data'],
        query={
            "script_score":{
                "query":{
                    "match":{
                        "data":query
                    }
                },
                "script":{
                    "source": """ (cosineSimilarity(params.query_vector, 'embeddings') +1)* params.encoder_boost + _score""",
                    "params":{
                        "query_vector": embeddings,
                        "encoder_boost": 10
                    },
                },
            }
        }
    )

    hits = results["hits"]['hits']
    data_results=[]
    for hit in hits:
        data_results.append({
            "Data":hit["_source"]["data"]
        })
    return data_results
# name = input("What is your name? ")
query = ("which is the capital of pakistan?")
data = query_data(query, "wikipedia_data")


answer = chat_bot(question=query, info=data)
print(answer)