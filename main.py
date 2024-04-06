import uvicorn
from fastapi import FastAPI

from app.adv.router import adv_router
from app.auth.router import auth_router
from app.users.router import user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(adv_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
