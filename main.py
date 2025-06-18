from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import blog, blogs
import models, database

app = FastAPI()

app.include_router(blog.router)
app.include_router(blogs.blogs_router)

models.database.Base.metadata.create_all(database.engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
