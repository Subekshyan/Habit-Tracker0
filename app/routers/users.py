from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)


@router.get("", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_or_404(db, user_id)


@router.patch("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, payload)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"message": f"User {user_id} deleted"}


@router.get("/{user_id}/freeze-tokens", response_model=List[schemas.FreezeTokenOut])
def list_freeze_tokens(user_id: int, db: Session = Depends(get_db)):
    return crud.list_freeze_tokens(db, user_id)
