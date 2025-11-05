from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from core.database import get_session, org_scope_query
from routers.marketplace import (item_router, org_router, template_router,
                                 user_router)
from schemas.marketplace import Item, Org, Template, User
from models import User as UserTable
from services.items import db_health_check

app = FastAPI()


@app.get("/health")
async def root(db: Session = Depends(get_session)):

    try:
        _ = db_health_check(db)
        print(f"Action Server Health Check completed")
        return {"status": "ok"}
    except Exception as e:
        print(f"Action Server Health Check failed")
        raise HTTPException(status_code=500, detail=f"DB connection failed: {str(e)}")



custom_user_router = APIRouter(prefix="/users", tags=["Users"])

crud_user = FastCRUD(UserTable)
# override Create route
@custom_user_router.post("/", summary="Create User for an Organization")
async def list_templates(
    user: User,  # or get from JWT later
    session: AsyncSession = Depends(get_session),
):

    password_hash = PasswordHash.recommended()
    user.password = password_hash.hash(user.password)

    user_db_obj = UserTable(**user.model_dump())
    # new_user = await crud_user.create(session=session, obj_in=user_db_obj)

    session.add(user_db_obj)

    await session.commit()
    await session.refresh(user_db_obj)


    return user_db_obj



app.include_router(org_router)
app.include_router(user_router)
app.include_router(custom_user_router)
app.include_router(template_router)
app.include_router(item_router)
