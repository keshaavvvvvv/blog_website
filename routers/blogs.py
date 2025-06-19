from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from typing import List
import os, shutil, glob, markdown
import models, database, schemas

blogs_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@blogs_router.get("/", response_model=List[schemas.Blog])
def list_all_blogs(request: Request, db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()

    return templates.TemplateResponse("home.html", {"request": request, "blogs": blogs})
