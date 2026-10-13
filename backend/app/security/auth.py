
import os

import firebase_admin
from firebase_admin import auth as firebase_auth
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer(auto_error=False)

FIREBASE_PROJECT_ID = os.getenv(
    "FIREBASE_PROJECT_ID",
    "regalis-ai-4f46e",
)


FIREBASE_APP_NAME = "regalis-auth"


def get_firebase_app():
    try:
        return firebase_admin.get_app(FIREBASE_APP_NAME)
    except ValueError:
        return firebase_admin.initialize_app(
            options={"projectId": FIREBASE_PROJECT_ID},
            name=FIREBASE_APP_NAME,
        )


firebase_app = get_firebase_app()


async def get_current_user(
    credentials=Depends(security),
):
    if os.getenv("ENVIRONMENT") == "development":
        return {
            "uid": "mock-user-123",
            "email": "dev@example.com",
            "name": "Development User",
        }

    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication credentials missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        decoded_token = firebase_auth.verify_id_token(
            credentials.credentials,
            app=firebase_app,
        )
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
