from fastapi import FastAPI
from app.core.config import settings
from app.routers import catalog, community, search, media, me


app = FastAPI(title="Shop+Community API", openapi_url=f"{settings.API_PREFIX}/openapi.json")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(catalog.router, prefix=settings.API_PREFIX)
app.include_router(community.router, prefix=settings.API_PREFIX)
app.include_router(search.router, prefix=settings.API_PREFIX)
app.include_router(media.router, prefix=settings.API_PREFIX)
app.include_router(me.router, prefix=settings.API_PREFIX)
