from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database

router = APIRouter(
    prefix="/blogs",
    tags=["Blog List"]
)

@router.get("/", response_model=List[schemas.Blog])
def list_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
