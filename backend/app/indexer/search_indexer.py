from opensearchpy import OpenSearch
from app.core.config import settings


_client: OpenSearch | None = None


def client() -> OpenSearch:
    global _client
    if _client is None:
        _client = OpenSearch(settings.OPENSEARCH_URL)
    return _client


def index_product(doc: dict):
    client().index(index="products", id=doc["id"], body=doc, refresh=True)


def index_thread(doc: dict):
    client().index(index="threads", id=doc["id"], body=doc, refresh=True)
