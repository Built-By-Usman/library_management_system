from fastapi import APIRouter,Depends
from typing import List
from database import getDb
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from repository.issue import get_issued_books,issue_book
from schemas import IssueReturnRM,IssueReturnSchema


router=APIRouter(
    prefix='/issue',
    tags=['Issue']
)

@router.get('/', response_model=List[IssueReturnRM])
def get_all(db: Session = Depends(getDb), current_user: get_current_user = Depends()):
    return get_issued_books(user_id=current_user.id, db=db)

@router.post('/',response_model=IssueReturnRM)
def add_issue(request:IssueReturnSchema,db:Session=Depends(getDb),current_user:get_current_user=Depends()):
    return issue_book(request=request,db=db,user_id=current_user.id)