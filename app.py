import csv

from io import StringIO

import jwt
from fastapi import (APIRouter, Depends, FastAPI, File, HTTPException, Security,
                     UploadFile)
from fastcrud import FastCRUD
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlmodel import select

from core.auth import create_access_token, verify_password, require_user
from core.config import settings
from core.database import get_session, org_scope_query
from models import OutboundItem as ItemTable
from models import Template as TemplateTable
from models import User as UserTable
from routers.marketplace import (item_router, org_router, template_router,
                                 user_router)
from schemas.marketplace import Item, Org, Template, User
from services.items import db_health_check

app = FastAPI()


@app.get("/health")
async def root(db: Session = Depends(get_session)):

    try:
        _ = db_health_check(db)
        print(f"Health Check completed")
        return {"status": "ok"}
    except Exception as e:
        print(f"Health Check failed")
        raise HTTPException(status_code=500, detail=f"DB connection failed: {str(e)}")

@app.get("/login")
async def root(user_id: str, password: str, session: AsyncSession = Depends(get_session)):

    try:

        if user_id == 'Dummy' and password == 'Dummy':
            access_token = create_access_token({"id":'Dummy'}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            return {"token": f"Bearer {access_token}"}

        # Fetching Templates for the Organization
        query = select(UserTable)
        query = query.where(UserTable.id == user_id)

        user = await session.execute(query)
        user = user.scalars().first()

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=403, detail=f"Wrong UserID or Password")
        
        access_token = create_access_token({"id":str(user.id)}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"token": f"Bearer {access_token}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


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

    session.add(user_db_obj)

    await session.commit()
    await session.refresh(user_db_obj)


    return user_db_obj


custom_items_router = APIRouter(prefix="/items", tags=["Items"])
@custom_items_router.post("/", summary="Bulk Upload of Items data, based on the Marketplace")
async def add_item(
    org_id: str,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):

    # Fetching Templates for the Organization
    query = select(TemplateTable)
    query = query.where(TemplateTable.org_id == org_id)

    templates = await session.execute(query)
    templates = templates.scalars().all()
    if templates == []:
        raise HTTPException("First Create Templates and then add Items")


    # Reading the file
    contents = await file.read()
    decoded_contents = contents.decode("utf-8")
    csv_file = StringIO(decoded_contents)
    reader = csv.DictReader(csv_file)

    # Creating DB Objects of Items
    item_list = []
    for row in reader:

        for template in templates:
            item_schema = {template.schema[k]:v for (k,v) in row.items()}
            template_id = template.id
            # item_pydantic = Item(org_id=org_id, template_id=template_id, data=item_schema, status='pushed')
            item_obj = ItemTable(org_id=org_id, template_id=template_id, data=item_schema, status='pushed')
            item_list.append(item_obj)


    session.add_all(item_list)
    await session.commit()

    return {"Status":"OK"}



app.include_router(org_router, dependencies=[Security(require_user)])
app.include_router(user_router, dependencies=[Security(require_user)])
app.include_router(custom_user_router, dependencies=[Security(require_user)])
app.include_router(template_router, dependencies=[Security(require_user)])
app.include_router(item_router, dependencies=[Security(require_user)])
app.include_router(custom_items_router, dependencies=[Security(require_user)])
app.include_router(custom_items_router, dependencies=[Security(require_user)])
