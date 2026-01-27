from pydantic import BaseModel, HttpUrl
from enum import Enum
from datetime import date
from typing import Optional


class IngredientItem(BaseModel):
  name: str
  quantity: str


class Difficulty(str, Enum): # Never use BaseModel with enum but str because that's easier for fastapi to return JSON
  EASY = "easy"
  MEDIUM = "medium"
  HARD = "hard"

class Category(str, Enum):
  BREAKFAST = "breakfast"
  LUNCH = "lunch"
  DINNER = "dinner"
  DESERT = "desert"
  SNACK = "snack"
  BEVERAGE = "beverage"


class Recipe(BaseModel):
  id: int
  title: str
  description: str
  ingredients: list[IngredientItem] # Nested Model
  instructions: list[str]
  prep_time: int
  cook_time: int
  servings: int
  difficulty: Difficulty # Since we are picking one item from Difficulty class
  category: Category
  image_url: Optional[HttpUrl] = None
  rating: int
  created_at: date
  updated_at: date


class RecipeCreate(BaseModel):
  title: str
  description: str
  ingredients: list[IngredientItem] # Nested Model
  instructions: list[str]
  prep_time: int
  cook_time: int
  servings: int
  difficulty: Difficulty
  category: Category
  image_url: Optional[HttpUrl] = None
  rating: int

# class RecipeCreate(BaseModel):
#   id: int
#   title: str
#   description: str
#   ingredients: list[IngredientItem] # Nested Model
#   instructions: str
#   prep_time: int
#   cook_time: int
#   servings: int
#   difficulty: list[Difficulty]
#   category: list[Category]
#   image_url: str
#   rating: int
  

