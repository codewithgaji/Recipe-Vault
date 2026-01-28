from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

Base = declarative_base()

class Recipe(Base):
  __tablename__ = "recipes"
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  title = Column(String)
  description = Column(String)
  instructions = Column(JSONB, nullable=False)
  prep_time = Column(Integer)
  cook_time = Column(Integer)
  servings = Column(Integer)
  difficulty = Column(String) 
  category = Column(String)
  image_url = Column(String)
  rating = Column(Integer)
  created_at = Column(Date, server_default=func.current_date())
  updated_at = Column(Date, server_default=func.current_date(), onupdate=func.current_date())

  ingredients = relationship(
    "Ingredient", 
    back_populates="recipe",
    cascade="all, delete-orphan"
  )

class Ingredient(Base):
  __tablename__ = "ingredients"
  
  id = Column(Integer, primary_key=True, index=True) # Every ingredient has it's own PK
  recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE")) # The Link with the "recipes" table, to Link the Id to the recipes.id. CASCADE to delete with all fields
  name = Column(String, nullable=False)
  quantity = Column(String, nullable=False)

  recipe = relationship("Recipe", back_populates="ingredients")