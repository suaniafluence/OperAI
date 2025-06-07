import httpx
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError

from .config import get_settings

settings = get_settings()

http_bearer = HTTPBearer()

async def get_jwks():
    url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(http_bearer),
):
    token = credentials.credentials
    jwks = await get_jwks()
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token header") from e

    key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)
    if not key:
        raise HTTPException(status_code=401, detail="Key not found")

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=header.get("alg", "RS256"),
            audience=settings.AUTH0_API_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Token verification failed") from e
    return payload
