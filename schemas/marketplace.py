from pydantic import BaseModel, Field
from typing import Dict


class Org(BaseModel):
    name: str
    prefix: str
    secret_name: str

class User(BaseModel):

    id: str = Field(...)
    org_id: str
    role: str

class Template(BaseModel):

    id: str
    org_id: str
    name: str
    schema: Dict

class Item(BaseModel):

    id: str
    org_id: str
    template_id: str
    data: Dict
    status: str
