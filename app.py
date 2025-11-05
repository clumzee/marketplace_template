from fastapi import FastAPI, Depends
from core import get_session
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
async def root(db: Session = Depends(get_session)):
    return {"message": "Hello World"}