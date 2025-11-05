from core.database import get_session
from fastcrud import FastCRUD, crud_router

from models import Org as OrgTable
from models import OutboundItem as ItemTable
from models import Template as TemplateTable
from models import User as UserTable
from schemas.marketplace import Item, Org, Template, User



org_router = crud_router(
    session=get_session,
    model=OrgTable,
    create_schema=Org,
    update_schema=Org,
    path="/orgs",
    tags=["Organization"],
)


user_router = crud_router(
    session=get_session,
    model=UserTable,
    create_schema=User,
    update_schema=User,
    path="/users",
    tags=["Users"],
    included_methods=['read', 'update']
)

template_router = crud_router(
    session=get_session,
    model=TemplateTable,
    create_schema=Template,
    update_schema=Template,
    path="/templates",
    tags=["Templates"],
)
item_router = crud_router(
    session=get_session,
    model=ItemTable,
    create_schema=Item,
    update_schema=Item,
    path="/items",
    tags=["Items"],
)
