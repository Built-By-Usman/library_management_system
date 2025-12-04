from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from modules.database import getDb
from models import BorrowReturnModel
from modules.schemas import BorrowReturnRM,BorrowReturnSchema
from typing import List
from modules.oauth2 import get_current_user
from modules.repository.returned import get,add



router=APIRouter(
    prefix='/return',
    tags=['Returned']
)

@router.get('/',response_model=List[BorrowReturnRM])
def get_all_return_book(db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return get(id=current_user.id,db=db,)


@router.post('/',response_model=BorrowReturnRM)
def add_return_book(request:BorrowReturnSchema,db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return add(request=request,db=db,id=current_user.id)