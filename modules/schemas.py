from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class UserSchema(BaseModel):
    name:str
    email:str
    password:str



class BookSchema(BaseModel):
    title:str
    author:str
    category:str
    ISBN:str
    copies:int
    user_id:int
    url:Optional[str] = None

class showUserBooks(BaseModel):
    id:int
    title:str
    author:str
    category:str
    ISBN:str
    copies:int
    user_id:int
    url:Optional[str] = None


class showUserRM(BaseModel):
    name:str
    email:str
    books:List[showUserBooks]

    model_config={
        "from_attributes":True
    }

class showOwnerRM(BaseModel):
    name:str
    email:str
    
    model_config={
        "from_attributes":True
    }


class showBookRM(BaseModel):
    id: int
    title: str
    author: str
    category: str
    ISBN: str             
    copies: int            
    owner: showOwnerRM
    url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class BorrowReturnSchema(BaseModel):
    book_id:int
    



class BorrowReturnRM(BaseModel):
    title:str
    author:str
    category:str
    owner:showOwnerRM
    book_id:int
    borrow_date: datetime
    return_date: datetime | None

    model_config={
        "from_attributes":True
    }




class LoginSchema(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

