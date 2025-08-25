import os
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY = os.getenv("API_KEY", "supersecret123")
API_KEY_HEADER = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)

async def get_api_key(api_key_header_value: str = Security(api_key_header)):
    if not api_key_header_value:
        raise HTTPException(status_code=401, detail="Missing API Key")
    if api_key_header_value != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_header_value
