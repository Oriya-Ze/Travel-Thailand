import time
import httpx
from typing import Any, Dict
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings


_jwks_cache: dict[str, Any] | None = None
_jwks_cache_exp: float = 0


def _jwks_url() -> str:
    return settings.OIDC_JWKS_URL or settings.COGNITO_JWKS_URL or ""


def _audience() -> str | None:
    return settings.OIDC_AUDIENCE or settings.COGNITO_AUDIENCE


async def _get_jwks() -> Dict[str, Any]:
    global _jwks_cache, _jwks_cache_exp
    now = time.time()
    if _jwks_cache and now < _jwks_cache_exp:
        return _jwks_cache

    url = _jwks_url()
    if not url:
        raise RuntimeError("JWKS URL not configured")

    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(url)
        r.raise_for_status()
        _jwks_cache = r.json()
        _jwks_cache_exp = now + 6 * 3600
        return _jwks_cache


bearer = HTTPBearer(auto_error=False)


async def get_current_claims(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> Dict[str, Any]:
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    token = creds.credentials
    jwks = await _get_jwks()
    aud = _audience()

    try:
        claims = jwt.decode(
            token,
            jwks,
            options={"verify_aud": bool(aud), "verify_at_hash": False},
            audience=aud,
            algorithms=["RS256"],
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    return claims

