from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # ✅ PyJWT
from jwt import InvalidTokenError
from app.application.services.user_service import UserService
from app.interfaces.http.schemas.user_schemas import UserCreateIn, UserOut, UserUpdateIn, PaginatedUsers

bearer = HTTPBearer(auto_error=True)

def get_users_router(user_service: UserService, jwt_secret: str, jwt_alg: str) -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    def _auth(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
        try:
            payload = jwt.decode(creds.credentials, jwt_secret, algorithms=[jwt_alg])
            return payload["sub"]
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="invalid token")

    @router.post("", response_model=UserOut, status_code=201)
    def create_user(body: UserCreateIn, _=Depends(_auth)):
        u = user_service.create_user(body.email, body.name, body.password)
        return UserOut(**u.__dict__)

    @router.get("/{user_id}", response_model=UserOut)
    def get_user(user_id: UUID, _=Depends(_auth)):
        u = user_service.get_user(user_id)
        if not u:
            raise HTTPException(status_code=404, detail="not found")
        return UserOut(**u.__dict__)

    @router.get("", response_model=PaginatedUsers)
    def list_users(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), _=Depends(_auth)):
        items, total = user_service.list_users(offset, limit)
        return PaginatedUsers(
            total=total, offset=offset, limit=limit,
            items=[UserOut(**u.__dict__) for u in items]
        )

    @router.patch("/{user_id}", response_model=UserOut)
    def update_user(user_id: UUID, body: UserUpdateIn, _=Depends(_auth)):
        u = user_service.update_user(user_id, body.name, body.password)
        return UserOut(**u.__dict__)

    @router.delete("/{user_id}", status_code=204)
    def delete_user(user_id: UUID, _=Depends(_auth)):
        user_service.delete_user(user_id)
        return

    return router
