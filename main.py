import uvicorn
from fastapi import FastAPI

from app.auth.router import auth_router
from app.users.router import user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
