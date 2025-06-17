from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix="/blog",
    tags=["Blog Operations"]
)

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
# def create_blog(request: schemas.UpBlog, db: Session = Depends(database.get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

@router.get("/{blog_id}", response_model=schemas.ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {blog_id} not found")
    return blog

@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: schemas.UpBlog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return {"message": "Blog updated successfully"}


