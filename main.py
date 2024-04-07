import uvicorn
from fastapi import FastAPI
from app.adv.router import adv_router
from app.auth.router import auth_router
from app.users.router import user_router

description = """
    **Advertisements**
    You will be able to use all CRUD operations with Advertisement (Adv) model
    
    **Comments**
    You can add new Comments or delete them to any Advertisement
    
    **Users**
    You will be able to use all CRUD operations with User model
    
    **Auth**
    Service offers JWT tokens is used for authorization 
"""
app = FastAPI(
    title="Advertising service",
    description=description,
    summary="Advertising service is a simple API of an advertisement board",
    version="1.0"
)

app.include_router(auth_router, tags=["Authorization"])
app.include_router(user_router, tags=["User"])
app.include_router(adv_router, tags=["Advertisement and Comment"])

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
