from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from qdrant_service.searcher import Searcher

from qdrant_service.config import IMG_COLLECTION_NAME, HAIKU_COLLECTION_NAME

img_searcher = Searcher(IMG_COLLECTION_NAME)
haiku_searcher = Searcher(HAIKU_COLLECTION_NAME)
img_vector_size = img_searcher.vector_size
haiku_vector_size = haiku_searcher.vector_size


tags_metadata = [
    {
        'name': 'imgs',
        'description': 'Similarity search on an image database.',
    },
    {
        'name': 'haiku',
        'description': 'Similarity search on a haiku database.',
    }
]

query_collection_description = 'Search by **query collection**: the collection \
                                can contain lists of texts and pre-embedded \
                                vectors. The resulting query vector will be an \
                                average of the vectors and text embeddings. \
                                Vectors have to be of dimensions {} for images \
                                and {} for haiku'.format(
                                    img_vector_size,
                                    haiku_vector_size
                                )

query_string_description = 'Search by **query text**: the text will be embedded \
                            and send to the database for similarity search.'


app = FastAPI(openapi_tags=tags_metadata)

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


class QueryCollection(BaseModel):
    texts: List[str] = []
    vectors: List[List[float]] = []


@app.get('/api/imgs/search', tags=['imgs'],
         description=query_string_description)
async def search_imgs_by_query_string(
    q: str,
    n: int = 10
) -> dict:
    return {'results': img_searcher.search(
        q_texts=[q],
        q_vectors=[],
        n_results=n
    )}

@app.get('/api/haiku/search', tags=['haiku'],
         description=query_string_description)
async def search_haiku_by_query_string(
    q: str,
    n: int = 10
) -> dict:
    return {'results': haiku_searcher.search(
        q_texts=[q],
        q_vectors=[],
        n_results=n
    )}


@app.post('/api/imgs/search', tags=['imgs'],
         description=query_collection_description)
async def search_imgs_by_query_collection(
    body: QueryCollection,
    n: int = 10
) -> dict:
    texts = body.texts
    vectors = body.vectors
    return {'results': img_searcher.search(
        q_texts=texts,
        q_vectors=vectors,
        n_results=n
    )}

@app.post('/api/haiku/search', tags=['haiku'],
         description=query_collection_description)
async def search_haiku_by_query_collection(
    body: QueryCollection,
    n: int = 10
) -> dict:
    texts = body.texts
    vectors = body.vectors
    return {'results': haiku_searcher.search(
        q_texts=texts,
        q_vectors=vectors,
        n_results=n
    )}


@app.get('/{full_path:path}')
async def list_endpoints() -> dict:
    endpoint_list = [{
        'path': route.path,
        'name': route.name
    } for route in app.routes]
    return {'message': 'see attached list for service endpoints',
            'endpoints': endpoint_list}
