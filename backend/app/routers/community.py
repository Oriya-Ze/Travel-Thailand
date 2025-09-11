from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.thread import Thread
from app.models.post import Post
from app.schemas.community import ThreadCreate, PostCreate
from app.deps.auth import get_current_claims


router = APIRouter(prefix="/community", tags=["community"])


@router.post("/threads")
def create_thread(payload: ThreadCreate, db: Session = Depends(get_db), claims: dict = Depends(get_current_claims)):
    user_id = claims.get("app_user_id") # אופציונלי: מיפוי claims->User.id
    t = Thread(title=payload.title, product_id=payload.product_id, created_by=user_id or 0)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"id": t.id, "title": t.title}


@router.post("/posts")
def create_post(payload: PostCreate, db: Session = Depends(get_db), claims: dict = Depends(get_current_claims)):
    user_id = claims.get("app_user_id") or 0
    if not db.get(Thread, payload.thread_id):
        raise HTTPException(404, "Thread not found")
    p = Post(thread_id=payload.thread_id, parent_post_id=payload.parent_post_id, body=payload.body, created_by=user_id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id}
