from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql import text



def db_health_check(db: Session):
    
    db.execute(text('SELECT 1'))
    return True

