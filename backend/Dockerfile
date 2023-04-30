FROM python:3.8-slim

ENV POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/src/qdrant_service

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
	&& poetry install --without dev --no-root --no-interaction --no-ansi \
  && rm -rf /root/.cache/pypoetry

# only include for testing purposes
# (-> huge image size but no download on container startup)
# RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1");'

COPY ./ ./
RUN poetry install --without dev --no-interaction --no-ansi

CMD ["uvicorn", "qdrant_service.service:app", "--host", "0.0.0.0", "--port", "8000"]
