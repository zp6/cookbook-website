from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, recipes

app = FastAPI(title="Cookbook API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])

@app.get("/")
def root():
    return {"message": "Cookbook API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
