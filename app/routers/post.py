from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db
from typing import List


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/",response_model=List[schemas.postResponse])
def get_posts(db: Session = Depends(get_db)):

    posts=db.query(models.post).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.postResponse)
def createpost(post:schemas.PostCreate,db: Session = Depends(get_db)):
    new_posts=models.post(**post.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)

    return new_posts


@router.get("/{id}",response_model=schemas.postResponse)
def get_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.post).filter(models.post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.post).filter(models.post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} does not exit")
    post.delete(synchronize_session=False) 
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.postResponse)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(models.post).filter(models.post.id==id)
    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} does not exit")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()