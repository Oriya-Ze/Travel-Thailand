from fastapi import APIRouter, Query
from app.indexer.search_indexer import client


router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(q: str = Query(...), scope: str = Query("products")):
    idx = "products" if scope == "products" else "threads"
    res = client().search(index=idx, body={"query": {"multi_match": {"query": q, "fields": ["title^2", "body", "brand"]}}})
    return res.get("hits", {})
