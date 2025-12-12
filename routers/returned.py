from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import getDb
from schemas import IssueReturnRM, ReturnSchema
from typing import List
from oauth2 import get_current_user
from repository.returned import get,add



router=APIRouter(
    prefix='/return',
    tags=['Returned']
)

@router.get('/',response_model=List[IssueReturnRM])
def get_all_return_book(db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return get(id=current_user.id,db=db,)


@router.post('/',response_model=IssueReturnRM)
def add_return_book(request:ReturnSchema,db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return add(request=request,db=db,id=current_user.id)