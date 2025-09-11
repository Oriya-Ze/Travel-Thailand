from fastapi import APIRouter, Depends
from app.deps.auth import get_current_claims


router = APIRouter(prefix="/me", tags=["auth"])


@router.get("")
async def me(claims=Depends(get_current_claims)):
    return {"sub": claims.get("sub"), "email": claims.get("email"), "groups": claims.get("cognito:groups", [])}
