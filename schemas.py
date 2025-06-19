from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    id: int
    image_filename: str = None

    class Config:
        orm_mode = True


class UpBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    image_filename: str = None

    class Config:
        orm_mode = True
