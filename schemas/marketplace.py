from typing import Dict, Literal

from pydantic import BaseModel, Field


class Org(BaseModel):
    name: str
    prefix: str
    secret_name: str

class User(BaseModel):

    org_id: str
    password: str
    role: Literal["member", "admin"]
    status: Literal["active", "inactive"]

class Template(BaseModel):

    org_id: str
    name: str
    schema: Dict

class Item(BaseModel):

    org_id: str
    template_id: str
    data: Dict
    status: str
