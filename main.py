from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import book, issue, user, login, returned


Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["index"])
def index():
    return {"detail": "This is the library management system"}

# Include routers
app.include_router(login.router)
app.include_router(user.router)
app.include_router(book.router)
app.include_router(issue.router)
app.include_router(returned.router)