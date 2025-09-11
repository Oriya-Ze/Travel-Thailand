from pydantic import BaseModel


class ThreadCreate(BaseModel):
    title: str
    product_id: int | None = None


class PostCreate(BaseModel):
    thread_id: int
    parent_post_id: int | None = None
    body: str
