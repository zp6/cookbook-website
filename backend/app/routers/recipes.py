from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Recipe
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: str
    instructions: str
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = "medium"
    author_id: int

class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    ingredients: str
    instructions: str
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    author_id: int

    class Config:
        from_attributes = True

@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

@router.get("/", response_model=list[RecipeResponse])
def list_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Recipe).offset(skip).limit(limit).all()

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
