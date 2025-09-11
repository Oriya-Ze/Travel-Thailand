import os, time, sys
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from opensearchpy import OpenSearch, NotFoundError

# ENV
DATABASE_URL = os.getenv("DATABASE_URL")                   # למשל: postgresql+psycopg://app:app@db:5432/shop
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL", "http://opensearch:9200")
OS_OPTIONAL = os.getenv("BOOTSTRAP_OS_OPTIONAL", "true").lower() == "true"

# ---------- DB ----------
def wait_for_db(url: str, retries: int = 60, delay: float = 2.0):
    last = None
    for i in range(1, retries + 1):
        try:
            eng = create_engine(url, pool_pre_ping=True)
            with eng.connect() as conn:
                conn.exec_driver_sql("SELECT 1")
            print(f"[bootstrap] DB ready after {i} tries")
            return
        except Exception as e:
            last = e
            time.sleep(delay)
    print(f"[bootstrap] DB not ready: {last}", file=sys.stderr)
    sys.exit(1)

def migrate():
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")

# ---------- OpenSearch ----------
PRODUCTS_MAPPING = {
    "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    "mappings": {"properties": {
        "id": {"type": "integer"},
        "title": {"type": "text"},
        "brand": {"type": "keyword"},
        "price": {"type": "float"},
        "stock": {"type": "integer"},
        "specs": {"type": "object", "enabled": True},
    }}
}
THREADS_MAPPING = {
    "settings": {"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    "mappings": {"properties": {
        "id": {"type": "integer"},
        "title": {"type": "text"},
        "product_id": {"type": "integer"},
    }}
}

def wait_for_opensearch(url: str, retries: int = 60, delay: float = 2.0) -> OpenSearch | None:
    last = None
    client = OpenSearch(url)
    for i in range(1, retries + 1):
        try:
            health = client.cluster.health()
            if health.get("status") in {"green", "yellow"}:
                print(f"[bootstrap] OpenSearch ready after {i} tries")
                return client
        except Exception as e:
            last = e
        time.sleep(delay)
    msg = f"[bootstrap] OpenSearch not ready: {last}"
    if OS_OPTIONAL:
        print(msg, file=sys.stderr)
        return None
    print(msg, file=sys.stderr)
    sys.exit(1)

def ensure_index(client: OpenSearch, name: str, body: dict):
    try:
        client.indices.get(name)
        print(f"[bootstrap] index '{name}' exists")
    except NotFoundError:
        client.indices.create(index=name, body=body)
        print(f"[bootstrap] index '{name}' created")

# ---------- main ----------
if __name__ == "__main__":
    print("[bootstrap] waiting for DB...")
    if not DATABASE_URL:
        print("[bootstrap] DATABASE_URL is not set", file=sys.stderr)
        sys.exit(1)
    wait_for_db(DATABASE_URL)

    print("[bootstrap] running migrations...")
    migrate()

    print("[bootstrap] waiting for OpenSearch...")
    os_client = wait_for_opensearch(OPENSEARCH_URL)
    if os_client is not None:
        ensure_index(os_client, "products", PRODUCTS_MAPPING)
        ensure_index(os_client, "threads", THREADS_MAPPING)

    print("[bootstrap] done")

