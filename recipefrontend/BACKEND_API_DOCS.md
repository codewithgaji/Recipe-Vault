# RecipeVault Backend API Documentation

This document contains everything you need to build the FastAPI backend for RecipeVault.

## Table of Contents
1. [API Endpoints](#api-endpoints)
2. [Pydantic Schemas](#pydantic-schemas)
3. [SQLAlchemy Models](#sqlalchemy-models)
4. [CORS Configuration](#cors-configuration)
5. [Frontend Integration Map](#frontend-integration-map)
6. [Example Request/Response](#example-requestresponse)
7. [Testing Checklist](#testing-checklist)

---

## API Endpoints

| Method | Route | Description | Request Body | Response |
|--------|-------|-------------|--------------|----------|
| GET | `/recipes` | List all recipes (with optional filters) | - | `Recipe[]` |
| GET | `/recipes/{id}` | Get a single recipe | - | `Recipe` |
| POST | `/recipes` | Create a new recipe | `RecipeCreate` | `Recipe` |
| PUT | `/recipes/{id}` | Update an existing recipe | `RecipeUpdate` | `Recipe` |
| DELETE | `/recipes/{id}` | Delete a recipe | - | `204 No Content` |

### Query Parameters for GET /recipes

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string (optional) | Search in title and description |
| `category` | string (optional) | Filter by category |
| `difficulty` | string (optional) | Filter by difficulty level |

---

## Pydantic Schemas

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Category(str, Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    dessert = "Dessert"
    snack = "Snack"
    beverage = "Beverage"


class IngredientItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    quantity: str = Field(..., min_length=1, max_length=100)


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    ingredients: List[IngredientItem] = Field(..., min_items=1)
    instructions: List[str] = Field(..., min_items=1)
    prep_time: int = Field(..., ge=0, description="Preparation time in minutes")
    cook_time: int = Field(..., ge=0, description="Cooking time in minutes")
    servings: int = Field(..., ge=1, description="Number of servings")
    difficulty: Difficulty
    category: Category
    image_url: Optional[str] = Field(None, max_length=500)
    rating: int = Field(..., ge=1, le=5)


class RecipeCreate(RecipeBase):
    """Schema for creating a new recipe"""
    pass


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    ingredients: Optional[List[IngredientItem]] = None
    instructions: Optional[List[str]] = None
    prep_time: Optional[int] = Field(None, ge=0)
    cook_time: Optional[int] = Field(None, ge=0)
    servings: Optional[int] = Field(None, ge=1)
    difficulty: Optional[Difficulty] = None
    category: Optional[Category] = None
    image_url: Optional[str] = Field(None, max_length=500)
    rating: Optional[int] = Field(None, ge=1, le=5)


class Recipe(RecipeBase):
    """Schema for recipe response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## SQLAlchemy Models

### Option 1: JSON Column (Simpler - Recommended for Learning)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class DifficultyEnum(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class CategoryEnum(enum.Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    dessert = "Dessert"
    snack = "Snack"
    beverage = "Beverage"


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Store arrays as JSON - simplest approach for learning
    ingredients = Column(JSON, nullable=False)  # List of {name, quantity} objects
    instructions = Column(JSON, nullable=False)  # List of strings
    
    prep_time = Column(Integer, nullable=False)
    cook_time = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(500), nullable=True)
    rating = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### Option 2: Normalized Tables (More Complex - Production Pattern)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    prep_time = Column(Integer, nullable=False)
    cook_time = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(500), nullable=True)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="recipe", cascade="all, delete-orphan", order_by="Instruction.step_number")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String(200), nullable=False)
    quantity = Column(String(100), nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")


class Instruction(Base):
    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    recipe = relationship("Recipe", back_populates="instructions")
```

---

## CORS Configuration

Add this to your FastAPI app:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RecipeVault API")

# CORS configuration for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Frontend Integration Map

| Frontend Function | File Location | API Endpoint Called |
|-------------------|---------------|---------------------|
| `recipeApi.getRecipes()` | `src/services/api.ts` | `GET /recipes` |
| `recipeApi.getRecipe(id)` | `src/services/api.ts` | `GET /recipes/{id}` |
| `recipeApi.createRecipe(data)` | `src/services/api.ts` | `POST /recipes` |
| `recipeApi.updateRecipe(id, data)` | `src/services/api.ts` | `PUT /recipes/{id}` |
| `recipeApi.deleteRecipe(id)` | `src/services/api.ts` | `DELETE /recipes/{id}` |

### React Query Hooks

| Hook | Purpose |
|------|---------|
| `useRecipes(filters)` | Fetch recipes with optional search/category/difficulty filters |
| `useRecipe(id)` | Fetch a single recipe by ID |
| `useCreateRecipe()` | Mutation for creating new recipes |
| `useUpdateRecipe()` | Mutation for updating existing recipes |
| `useDeleteRecipe()` | Mutation for deleting recipes |

---

## Example Request/Response

### POST /recipes - Create Recipe

**Request:**
```json
{
  "title": "Classic Pancakes",
  "description": "Fluffy buttermilk pancakes that are perfect for a lazy weekend breakfast.",
  "ingredients": [
    { "name": "All-purpose flour", "quantity": "2 cups" },
    { "name": "Buttermilk", "quantity": "1.5 cups" },
    { "name": "Eggs", "quantity": "2 large" },
    { "name": "Butter, melted", "quantity": "3 tbsp" },
    { "name": "Sugar", "quantity": "2 tbsp" },
    { "name": "Baking powder", "quantity": "2 tsp" },
    { "name": "Salt", "quantity": "1/2 tsp" }
  ],
  "instructions": [
    "Mix flour, sugar, baking powder, and salt in a large bowl.",
    "In another bowl, whisk together buttermilk, eggs, and melted butter.",
    "Pour wet ingredients into dry ingredients and stir until just combined (lumps are okay!).",
    "Heat a griddle or pan over medium heat and lightly grease.",
    "Pour 1/4 cup batter per pancake. Cook until bubbles form, then flip.",
    "Cook until golden brown on both sides. Serve warm with maple syrup."
  ],
  "prep_time": 10,
  "cook_time": 20,
  "servings": 4,
  "difficulty": "easy",
  "category": "Breakfast",
  "image_url": "https://example.com/pancakes.jpg",
  "rating": 5
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Classic Pancakes",
  "description": "Fluffy buttermilk pancakes that are perfect for a lazy weekend breakfast.",
  "ingredients": [
    { "name": "All-purpose flour", "quantity": "2 cups" },
    { "name": "Buttermilk", "quantity": "1.5 cups" },
    { "name": "Eggs", "quantity": "2 large" },
    { "name": "Butter, melted", "quantity": "3 tbsp" },
    { "name": "Sugar", "quantity": "2 tbsp" },
    { "name": "Baking powder", "quantity": "2 tsp" },
    { "name": "Salt", "quantity": "1/2 tsp" }
  ],
  "instructions": [
    "Mix flour, sugar, baking powder, and salt in a large bowl.",
    "In another bowl, whisk together buttermilk, eggs, and melted butter.",
    "Pour wet ingredients into dry ingredients and stir until just combined (lumps are okay!).",
    "Heat a griddle or pan over medium heat and lightly grease.",
    "Pour 1/4 cup batter per pancake. Cook until bubbles form, then flip.",
    "Cook until golden brown on both sides. Serve warm with maple syrup."
  ],
  "prep_time": 10,
  "cook_time": 20,
  "servings": 4,
  "difficulty": "easy",
  "category": "Breakfast",
  "image_url": "https://example.com/pancakes.jpg",
  "rating": 5,
  "created_at": "2025-01-22T10:30:00Z",
  "updated_at": "2025-01-22T10:30:00Z"
}
```

### GET /recipes?category=Breakfast&difficulty=easy

**Response:**
```json
[
  {
    "id": 1,
    "title": "Classic Pancakes",
    "description": "Fluffy buttermilk pancakes...",
    "ingredients": [...],
    "instructions": [...],
    "prep_time": 10,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "easy",
    "category": "Breakfast",
    "image_url": "https://example.com/pancakes.jpg",
    "rating": 5,
    "created_at": "2025-01-22T10:30:00Z",
    "updated_at": "2025-01-22T10:30:00Z"
  }
]
```

### PUT /recipes/1 - Partial Update

**Request:**
```json
{
  "rating": 4,
  "prep_time": 15
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Classic Pancakes",
  "description": "Fluffy buttermilk pancakes...",
  "...": "...",
  "prep_time": 15,
  "rating": 4,
  "updated_at": "2025-01-22T11:00:00Z"
}
```

### DELETE /recipes/1

**Response:** `204 No Content`

---

## Testing Checklist

### Basic CRUD
- [ ] POST /recipes - Create a recipe with all required fields
- [ ] POST /recipes - Validate required fields return 422
- [ ] GET /recipes - Returns empty array when no recipes
- [ ] GET /recipes - Returns all recipes
- [ ] GET /recipes/{id} - Returns single recipe
- [ ] GET /recipes/{id} - Returns 404 for non-existent ID
- [ ] PUT /recipes/{id} - Updates only provided fields
- [ ] PUT /recipes/{id} - Returns 404 for non-existent ID
- [ ] DELETE /recipes/{id} - Deletes recipe successfully
- [ ] DELETE /recipes/{id} - Returns 404 for non-existent ID

### Filtering
- [ ] GET /recipes?search=pancake - Searches title and description
- [ ] GET /recipes?category=Breakfast - Filters by category
- [ ] GET /recipes?difficulty=easy - Filters by difficulty
- [ ] GET /recipes?search=egg&category=Breakfast - Multiple filters work together

### Validation
- [ ] Title max length 200 characters
- [ ] At least 1 ingredient required
- [ ] At least 1 instruction required
- [ ] Rating between 1-5
- [ ] Difficulty must be easy/medium/hard
- [ ] Category must be valid enum value

### Array Fields
- [ ] Ingredients stored and retrieved correctly
- [ ] Instructions stored and retrieved in order
- [ ] Empty arrays rejected
- [ ] Partial updates to arrays work correctly

### Edge Cases
- [ ] Very long description (1000 chars)
- [ ] Unicode characters in title/description
- [ ] Optional image_url can be null
- [ ] prep_time and cook_time can be 0

---

## Quick Start for FastAPI

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RecipeVault API")

# Add CORS middleware here (see above)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recipes", response_model=List[schemas.Recipe])
def get_recipes(
    search: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)
    
    if search:
        query = query.filter(
            models.Recipe.title.ilike(f"%{search}%") |
            models.Recipe.description.ilike(f"%{search}%")
        )
    if category:
        query = query.filter(models.Recipe.category == category)
    if difficulty:
        query = query.filter(models.Recipe.difficulty == difficulty)
    
    return query.all()


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.post("/recipes", response_model=schemas.Recipe, status_code=201)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=[i.model_dump() for i in recipe.ingredients],
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty.value,
        category=recipe.category.value,
        image_url=recipe.image_url,
        rating=recipe.rating
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeUpdate,
    db: Session = Depends(get_db)
):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    update_data = recipe.model_dump(exclude_unset=True)
    
    # Handle enum conversions
    if "difficulty" in update_data and update_data["difficulty"]:
        update_data["difficulty"] = update_data["difficulty"].value
    if "category" in update_data and update_data["category"]:
        update_data["category"] = update_data["category"].value
    if "ingredients" in update_data and update_data["ingredients"]:
        update_data["ingredients"] = [i.model_dump() for i in recipe.ingredients]
    
    for field, value in update_data.items():
        setattr(db_recipe, field, value)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return None
```

---

## Notes on Array Fields in SQLAlchemy

### Using JSON Column (Recommended for SQLite/PostgreSQL)

The JSON column type works well for storing arrays:

```python
# Storing
recipe.ingredients = [{"name": "flour", "quantity": "2 cups"}]
recipe.instructions = ["Step 1", "Step 2"]

# Querying
# Note: JSON queries vary by database
# SQLite: Use json_extract
# PostgreSQL: Use native JSON operators
```

### Important Considerations

1. **Validation**: Always validate array contents in Pydantic before storing
2. **Ordering**: Instructions order is preserved in JSON arrays
3. **Searching**: Full-text search in JSON requires database-specific functions
4. **Migrations**: JSON schema changes need careful handling

### Common Patterns

```python
# Converting Pydantic models to dicts for JSON storage
ingredients_json = [i.model_dump() for i in recipe.ingredients]

# Converting JSON back to Pydantic models (for validation)
ingredients = [IngredientItem(**i) for i in db_recipe.ingredients]
```

---

Happy coding! 🚀
