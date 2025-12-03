from fastapi import FastAPI
from modules.database import Base,engine
from routers import book,user,login,borrow,returned



Base.metadata.create_all(engine)

app=FastAPI()





@app.get("/",tags=["index"])
def index():
    return {"detail":"This is the library management system"}

app.include_router(login.router)

app.include_router(user.router)

app.include_router(book.router)

app.include_router(borrow.router)

app.include_router(returned.router)





