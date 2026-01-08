from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schema, models, utils
from app.database import get_db, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello EV Charging World"}


@app.get("/users", response_model=List[schema.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/users/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@app.post("/users", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with email {user.email} already exists.')
    
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(
        **(user.model_dump())
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: schema.UserBase, db: Session = Depends(get_db)):
    deleted_user = db.query(models.User).filter(models.User.email == user.email).first()

    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {user.email} does not exist.')

    db.delete(deleted_user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

