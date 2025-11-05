from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastcrud import FastCRUD, crud_router
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import get_session
from routers.marketplace import item_router, org_router, template_router, user_router
from schemas.marketplace import Item, Org, Template, User
from models import User as UserTable, OutboundItem as ItemTable, Template as TemplateTable, Org as OrgTable
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


# app.include_router(CRUDRouter(schema=User))
# app.include_router(CRUDRouter(schema=Org))
# app.include_router(CRUDRouter(schema=Item))
# app.include_router(CRUDRouter(schema=Template))


app.include_router(org_router)
app.include_router(user_router)
app.include_router(template_router)
app.include_router(item_router)
