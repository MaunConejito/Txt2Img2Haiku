from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from qdrant_service.image_searcher import ImageSearcher

app = FastAPI()

origins = [
    '*'
]

img_searcher = ImageSearcher()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/api/flowers/search')
async def search_flowers(q: str, n: int) -> dict:
    endpoint_list = [{'path': route.path, 'name': route.name} \
                    for route in app.routes]
    return {'query': q,
            'results': img_searcher.search(text=q, n_results=n)}


@app.get('/{full_path:path}')
async def list_endpoints() -> dict:
    endpoint_list = [{'path': route.path, 'name': route.name} \
                    for route in app.routes]
    return {'message': 'see attached list for service endpoints',
            'endpoints': endpoint_list}
