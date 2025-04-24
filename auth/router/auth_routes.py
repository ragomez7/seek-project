from fastapi import APIRouter, HTTPException
from datetime import datetime
from auth.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from auth.utils import hash_password, verify_password, create_access_token
import os
from db import client

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register_user(data: UserRegisterRequest):
    if client.tasksdb.users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = {
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "created_at": datetime.utcnow()
    }
    result = client.tasksdb.users.insert_one(user)
    token = create_access_token({"sub": data.email})
    return TokenResponse(
        access_token=token,
        user_id=str(result.inserted_id)
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(data: UserLoginRequest):
    user = client.tasksdb.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["email"]})
    return TokenResponse(
        access_token=token,
        user_id=str(user["_id"])
    )
