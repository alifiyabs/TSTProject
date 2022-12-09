from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from fastapi import status, HTTPException, APIRouter, Depends
from authentication.hash_password import Hash
from database import database

router = APIRouter(tags=["Users"])

get_db = database.get_db

@router.post('/users')
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    ada_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if ada_user:
        return {"Message": "Email already in use"}
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users')
def retrieve_user(db: Session = Depends(get_db)):
    user = db.query(models.User.email).all()
    return user

@router.get('/users/{id}')
def retrieve_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User.email).filter(models.User.id == id).first()
    return user

@router.delete('/users/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User dengan id {id} tidak ada")
    user.delete(synchronize_session=False)
    db.commit()
    return {"Message": f"user dengan id {id} telah dihapus"}