
# Txt2Img2Haiku
Txt2Img2Haiku is a tiny web application demonstrating the possibilities of cross-media semantic search utilizing vector similarity search and an [ANN](## "Artificial Neural Network") model capable of vector-embedding texts **and** images. It consists of a frontend application (React) and a webservice (FastAPI) using a cloud-hosted vector search engine (Qdrant Cloud).

### Table of Contents
1. [Background](#background)
2. [Idea](#idea)
3. [Realization](#realization)
4. [Run this App](#run-this-app)

## Background
ANNs can be trained to convert texts, images or any other input into vector representations, mapping semantic similarity of the input to proximity in the result vector space[^1]. Converting input data into an vector in this way is called _embedding_. This enables a new way of searching for content: provided you have a collection of texts or images or any other kind of data, and a pretrained ANN that allows the embedding of that specific data format, you could now convert (embed) the collection into a set of vectors. Searching for items that are semantically similar to a _query item_ then breaks down into 1. embedding the query item and 2. searching for those vectors closest to the resulting _query vector_.

One of the advantages of this approach (as opposed to conventional text search using _indices_) is that it is less about the **actual words** of the query rather than its **meaning**. Take for example the queries 'puppy taking a nap' and 'sleeping baby dog'. In basic conventional text search, these queries could yield totally different results (because all of the actual words are different). Using embedding and vector similarity search though, the resulting query vectors would be very similar due to the semantic similarity of the sentences. The search would thus return the same or very similar results.

Another fairly exciting advantage is the possibility of _cross-media search_. Since search operations always take place in an abstract vector space - oblivious to the actual data the vectors are representing - you can easily search for a text using either another text as a query, or an image, or an audio file, ... or any combination thereof[^2]! The difficulty then lies in the design of a model (more specifically co-design of several models) that allows for the embedding of those different data types into the same semantic vector space.

[^1]: Definitions of vector distance can vary. See for example [here](https://qdrant.tech/documentation/search/#metrics).
[^2]: Using semantic operations on the resulting query vectors.

## Idea
With the possibility to embed different media types into the same semantic vector space (using the right model) comes the possibility of using _multi-media queries_. You can search for content using for example both text **and** images. What could that be useful for?

Images can carry very nuanced information that might be easy for humans to grasp in a single view of given image but hard to describe using words. A search query using such an image has the potential to return more precise results. In some search scenarios it might thus be helpful to **refine a textual search query with images**: based on an initial textual query, a set of images (semantically similar to the query) can be presented to the user who may then select one or more of these images. A combination of their embeddings can then be used as a new query vector.

While for some applications this approach might be promising - searching for a place to spend your holidays, for poetic literature or interior design ideas - in other cases it is definitely not. A search for rather abstract information (legal advice, mathematics, ...) or a specific event or location would probably not profit from a search refinement using images. Anyway, it is worth a try!

## Realization

A fitting test scenario is the search for [_Haiku_](https://en.wikipedia.org/wiki/Haiku). Haiku are - in short - tiny poems, which makes them a good candidate for visual search query refinement (since they are poems) and easy to handle from a data science perspective (since they are tiny).

For building a test application, four components are needed: A haiku database, an image database, an ANN model capable of embedding both text and images into the same semantic vector space and a vector search engine.

### Data

All haiku were taken from [this GitHub repository](https://github.com/docmarionum1/haikurnn) (_haikurnn_ by [Jeremy Neiman](https://github.com/docmarionum1)) providing a collection of over 300.000 haiku from different sources. (The collection includes some rather nonsensical haiku. Take for example this masterpiece: "i - col - i")

The Images stem from the [Open Images V7](https://storage.googleapis.com/openimages/web/index.html) dataset, chosen mainly for the generality of the included images.

### Model

The model used for embedding is [CLIP](https://huggingface.co/sentence-transformers/clip-ViT-B-32-multilingual-v1), a model trained on image-text pairs and capable of transforming both text and images into a common vector space. One of the major restrictions of this model is the text size it is capable of processing (since it is not optimized for text processing but rather). In the specific version used, it is constrained to [77 _word pieces_](https://github.com/UKPLab/sentence-transformers/issues/1269). This is one of the reasons why haiku are well fit as test data.

### Vector Search Engine

The search engine used is [Qdrant](https://qdrant.tech/), offering a [cloud hosted solution](https://cloud.qdrant.io/) (free up to 1GB). You can use either its API or a Python client to upload a collection of vector-payload-pairs and then perform searches on it by submitting query vectors.

## Run this App

### Requirements

* You will need to have set up a free cluster at [Qdrant Cloud](https://cloud.qdrant.io)
*  and installed [Python](https://www.python.org/downloads/) as well as either ...
	* [Docker](https://docs.docker.com/get-docker/)
	or
	* [Node.js](https://nodejs.org/en/download)

### Preparation

* Download or clone this repository
* create a file called `secrets.env` in the project's root folder and add your Qdrant cluster credentials like this:
	```
	QDRANT_CLUSTER_URL=<cluster-url>
	QDRANT_CLUSTER_TOKEN=<api-token>
	```

#### Prepare Data and Initialize Cluster

Run `$ pip install /path/to/data_init/`. After installation run the `initialize_data.py` script: `$ python /path/to/initialize_data.py` (try the `-h` flag for available options).

This will take a while since images and haiku have to be downloaded, embedded and uploaded to the cluster. For testing, limit the number of handled images and haiku with `--max_imgs` (default 5000) and `--max_haiku`.

### Install and Run Locally

Note: After startup, frontend and backend should be available at the addresses specified in the `.env` file.
> If you change `LOCAL_BACKEND_ADDRESS` in `.env`, also change `SERVICE_URL` in `frontend/frontend.local.env` accordingly.

After backend startup you can view an API specification at `<backend_url>/docs`.

#### Docker

In the terminal navigate to the project's root folder and run `$ docker compose up`. (You might have to grant privileges by using e.g. `sudo` on linux). After building the required Docker-images (this will take a while), frontend and backend will automatically be started as separate containers.

#### Manual Installation

Install by running `$ npm install /path/to/frontend/` and `$ pip install /path/to/backend/`.

After installation, run `python /path/to/backend/main.py` to start backend and ``npm start --prefix path/to/frontend/`` to start frontend.
