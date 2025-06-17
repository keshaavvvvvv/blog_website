from fastapi import FastAPI,Request,Form,HTTPException
from fastapi import APIRouter, Depends ,FastAPI,Request
from sqlalchemy.orm import Session
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routers import blog
import models, database,schemas


app = FastAPI()

models.database.Base.metadata.create_all(database.engine)
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/blogs",
    tags=["Blog List"]
)

@app.get("/", response_model=List[schemas.Blog])
def list_all_blogs(request : Request ,db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()

    return templates.TemplateResponse("home.html", {"request": request, "blogs": blogs})




@app.get("/create-blog")
def show_create_blog_form(request: Request):
    return templates.TemplateResponse("create-blog.html", {"request": request})





@app.post("/create-blog")
def submit_blog_form(request: Request,title: str = Form(...),body: str = Form(...),db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=title, body=body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return RedirectResponse(url="/", status_code=303)

# Register both routers
app.include_router(blog.router)


@app.get("/delete-blog")
def delete_blog_form(request: Request):
    return templates.TemplateResponse("delete-blog.html", {"request": request})

@app.post("/delete-blog")
def delete_blog(request: Request, blog_id: int = Form(...), db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return RedirectResponse(url="/", status_code=303)



@app.get("/edit-blog-id")
def get_blog_id_input(request: Request):
    return templates.TemplateResponse("edit-blog-id.html", {"request": request})

@app.get("/edit-blog")
def show_edit_form(request: Request, blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return templates.TemplateResponse("edit-blog.html", {"request": request, "blog": blog})


@app.post("/edit-blog/{blog_id}")
def update_blog(blog_id: int, title: str = Form(...), body: str = Form(...), db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.title = title
    blog.body = body
    db.commit()
    return RedirectResponse(url="/", status_code=303)