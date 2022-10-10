import math
import json
import heapq
from collections import defaultdict
from elasticsearch import Elasticsearch


ES_URL = 'http://elasticsearch:9200'
ES_INDEX = 'netflix'
DOC_TYPE = '_doc'

es = Elasticsearch(ES_URL)

def recommend(user):
    request_body = {
        "_source": {
            "includes": ["user", "movie_id", "method"],
        },
        "query": {
            "bool": {
                "must": [
                    {"match": {"user": f'{user}'}},
                    {"match": {"method": "GET"}}
                ]
            }
        }
    }

    res = es.search(index=ES_INDEX, body=request_body)

    with open('/opt/json_file/movie_list.json', 'r') as fh:
        movie_dict = json.load(fh)

    nation_counter = defaultdict(int)
    genre_counter = defaultdict(int)
    movie_id_set = set()

    for i in range(len(res.body['hits']['hits'])):
        record = res.body['hits']['hits'][i]['_source']
        movie_id = record['movie_id']
        nation = movie_dict[movie_id]['nation']
        genre = movie_dict[movie_id]['genre']
        
        nation_counter[nation] += 1
        genre_counter[genre] += 1
        movie_id_set.add(movie_id)

    top_2_nation = heapq.nlargest(2, nation_counter, key=nation_counter.get)
    top_2_genre = heapq.nlargest(2, genre_counter, key=genre_counter.get)

    my_favorite_type_list = []
    for nat in top_2_nation:
        for gen in top_2_genre:
            my_favorite_type_list.append((nat, gen))

    recommend_list = []


    for nat, gen in my_favorite_type_list:
        for movie_id, movie_info in movie_dict.items():
            if movie_info['nation'] == nat and movie_info['genre'] == gen:
                recommend_list.append(movie_dict[movie_id]['title'])
                print(f"{user}님 지금 {movie_dict[movie_id]['title']} 영화 추천드려요!")

    return recommend_list