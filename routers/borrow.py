from fastapi import APIRouter,Depends
from typing import List
from modules.database import getDb
from sqlalchemy.orm import Session
from modules.oauth2 import get_current_user
from modules.repository.borrow import get,create
from modules.schemas import BorrowReturnSchema,BorrowReturnRM


router=APIRouter(
    prefix='/borrow',
    tags=['Borrow']
)

@router.get('/',response_model=List[BorrowReturnRM])
def getAll(db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return get(id=current_user.id,db=db)

@router.post('/',response_model=BorrowReturnRM)
def addBorrow(request:BorrowReturnSchema,db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return create(request=request,db=db,user_id=current_user.id)