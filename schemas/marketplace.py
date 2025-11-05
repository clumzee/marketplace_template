from pydantic import BaseModel, Field
from typing import Dict


class Org(BaseModel):
    name: str
    prefix: str
    secret_name: str

class User(BaseModel):

    org_id: str
    role: str
    status: str

class Template(BaseModel):

    org_id: str
    name: str
    schema: Dict

class Item(BaseModel):

    org_id: str
    template_id: str
    data: Dict
    status: str
