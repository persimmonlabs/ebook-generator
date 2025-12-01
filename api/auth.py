"""JWT Authentication and Admin verification using Supabase."""
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
from typing import Optional

from .config import settings

# auto_error=False prevents 403 on preflight OPTIONS requests
security = HTTPBearer(auto_error=False)


async def verify_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> str:
    """
    Verify JWT token and check admin role.

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        user_id if valid admin

    Raises:
        HTTPException 401: Invalid or expired token
        HTTPException 403: User is not an admin
    """
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Decode Supabase JWT
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    # Check admin role in profiles table (using service role to bypass RLS)
    try:
        supabase = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
        )
        result = (
            supabase.table("profiles")
            .select("role")
            .eq("id", user_id)
            .single()
            .execute()
        )

        if not result.data or result.data.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to verify admin role: {str(e)}"
        )

    return user_id
