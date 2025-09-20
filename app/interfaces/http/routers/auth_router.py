from fastapi import APIRouter, HTTPException
from app.interfaces.http.schemas.auth_schemas import LoginIn, TokenOut
from app.application.services.user_service import UserService
from app.application.ports.auth_service import AuthService

def get_auth_router(user_service: UserService, auth: AuthService) -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/login", response_model=TokenOut)
    def login(body: LoginIn):
        user = user_service.repo.get_by_email(body.email)
        if not user or not auth.verify_password(body.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="invalid credentials")
        token = auth.create_access_token(sub=str(user.id))
        return TokenOut(access_token=token)

    return router
