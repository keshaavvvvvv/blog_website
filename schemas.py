from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
  title : str
  body : str
  id : int
  class Config():
    orm_mode =True

class UpBlog(BaseModel):
  title : str
  body : str
  class Config():
    orm_mode =True

class ShowBlog(BaseModel):
  title : str
  body : str
  class Config():
      orm_mode = True

