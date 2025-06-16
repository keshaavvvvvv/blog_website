from fastapi import FastAPI
from routers import blog,blogs
import models, database

app = FastAPI()

models.database.Base.metadata.create_all(database.engine)

# Register both routers
app.include_router(blog.router)
app.include_router(blogs.router)
