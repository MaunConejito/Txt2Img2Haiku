from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from qdrant_service.searcher import Searcher

from qdrant_service.config import IMG_COLLECTION_NAME, HAIKU_COLLECTION_NAME

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


img_searcher = Searcher(IMG_COLLECTION_NAME)
haiku_searcher = Searcher(HAIKU_COLLECTION_NAME)

class QueryCollection(BaseModel):
    texts: List[str] = []
    vectors: List[List[float]] = []

@app.get('/api/imgs/search')
async def get_search_imgs(q: str, n: int) -> dict:
    return {'query': q,
            'results': img_searcher.search(texts=[q],\
                        vectors=[], n_results=n)}

@app.get('/api/haikus/search')
async def get_search_haikus(q: str, n: int) -> dict:
    return {'query': q,
            'results': haiku_searcher.search(texts=[q],\
                        vectors=[], n_results=n)}

@app.post('/api/imgs/search')
async def post_search_imgs(body: QueryCollection, n: int) -> dict:
    texts = body.texts
    vectors = body.vectors
    return {'results': img_searcher.search(texts=texts,\
                        vectors=vectors, n_results=n)}

@app.post('/api/haikus/search')
async def post_search_haikus(body: QueryCollection, n: int) -> dict:
    texts = body.texts
    vectors = body.vectors
    return {'results': haiku_searcher.search(texts=texts,\
                        vectors=vectors, n_results=n)}


@app.get('/{full_path:path}')
async def list_endpoints() -> dict:
    endpoint_list = [{'path': route.path, 'name': route.name} \
                    for route in app.routes]
    return {'message': 'see attached list for service endpoints',
            'endpoints': endpoint_list}
