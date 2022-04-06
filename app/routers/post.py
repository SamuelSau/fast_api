from app import oath2
from .. import models, schema
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter( #routers allow us to breakdown our code into different files without having to write it all to app file
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), 
get_current_user: int = Depends(oath2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""): #basically the database dependency that allows us to reference database.py and create a session
    
    #cursor.execute("SELECT * FROM posts") #query execution from psycop
    #posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #dont need to write out SQL in the code, let SQLalchemy handle it for us. We can specify our filters for our query parameters.     
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

    #return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post) #path operation at the URL indicated
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oath2.get_current_user)):
    
    new_post = models.Post(owner_id = get_current_user.id, **post.dict()) #unpacks dictionary so that it structures it for us

    #cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published)) #deters SQL injection
    #new_post = cursor.fetchone()
    #conn.commit()
    
    print(get_current_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#title str, content str, <-schema (rules for how data should be sent/expected for users) used with pydantic
#wautomatic validation for schema when using pydantic :D
#basically new_post is a pydantic model

@router.get("/{id}", response_model=schema.PostOut) #id is a path parameter, must manually convert path parameter since it automatically assumes string
def get_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oath2.get_current_user)):
    
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id))) #%s helps prevent SQL injection
    #post = cursor.fetchone()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post

#deleting post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oath2.get_current_user)):

    #find index in array with required id
    #my_posts.pop(index)
    
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    else:
        post_query.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oath2.get_current_user)): #no need to create another model called UpdatePost since it will be exactly the same
    
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ",
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    else:
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()

    return post_query.first()