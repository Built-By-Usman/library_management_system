from fastapi import Depends
from fastapi import APIRouter
from typing import List
from schemas import BookSchema,showBookRM,showUserRM
from sqlalchemy.orm import Session
from database import getDb
from oauth2 import get_current_user
from repository.book import all,create,update


router=APIRouter(
    prefix='/book',
    tags=['Books']
)
# current_user:showUserRM=Depends(get_current_user)

@router.get("/",response_model=List[showBookRM])
def get_all_books(db:Session=Depends(getDb),current_user:showUserRM=Depends(get_current_user)):
    return all(db)
   


@router.post('/',response_model=showBookRM)
def add_book(request:BookSchema,db:Session=Depends(getDb),current_user:showUserRM=Depends(get_current_user)):
    return create(request=request,db=db)


@router.put('/{id}')
def update_book(id:int,request:BookSchema,db:Session=Depends(getDb),current_user:showUserRM=Depends(get_current_user)):
    return update(id=id,request=request,db=db)

