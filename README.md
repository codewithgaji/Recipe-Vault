# 📚 Recipe Vault – Full Stack Recipe Management API

Recipe Vault is a full-stack recipe management system built with FastAPI, SQLAlchemy, PostgreSQL, and integrated with Cloudinary for image hosting. It supports nested data models (recipes with ingredients), enum-based validation, JSON-based instructions, and complete CRUD operations connected to a React frontend.

---

## 🚀 Features

- Create, read, update, delete recipes
- Nested ingredients system (one-to-many relationship)
- Enum validation for difficulty level and category
- Instructions stored as a list (JSON)
- Image uploads via Cloudinary
- Automatic database seeding
- Clean API structure
- Frontend-ready responses

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy ORM** - Database toolkit
- **PostgreSQL** - Relational database
- **Pydantic v2** - Data validation
- **Cloudinary SDK** - Image hosting
- **Python-dotenv** - Environment management

### Frontend (separate repo)
- **React + Vite** - UI framework
- **TypeScript** - Type safety

---

## 📁 Project Structure

```
backend/
│
├── main.py                  # FastAPI application entry point
├── database.py              # Database connection setup
├── database_models.py       # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── cloudinary_config.py     # Cloudinary configuration
├── upload_images.py         # Bulk image upload script
├── .env                     # Environment variables
└── assets/                  # Local image assets
```

---

## 🧱 Database Design

### Recipe Table
- `id` (PK)
- `title`
- `description`
- `instructions` (JSON list)
- `prep_time`
- `cook_time`
- `servings`
- `difficulty` (enum as string)
- `category` (enum as string)
- `image_url`
- `rating`
- `created_at`
- `updated_at`

### Ingredient Table
- `id` (PK)
- `recipe_id` (FK → recipes.id)
- `name`
- `quantity`

### Relationship
```
Recipe 1 ---- * Ingredient
```

---

## 📜 Pydantic Models

- Nested `IngredientItem` model
- Enum validation for `Category` and `Difficulty`
- Instructions stored as `list[str]`
- Optional fields for updates

### Example:

```python
class Recipe(BaseModel):
    title: str
    description: str
    ingredients: list[IngredientItem]
    instructions: list[str]
    prep_time: int
    cook_time: int
    servings: int
    difficulty: Difficulty
    category: Category
    image_url: str | None
    rating: int
```

---

## ☁️ Cloudinary Integration

Images are uploaded to Cloudinary and stored as URLs in the database.

### Config file (cloudinary_config.py)
```python
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
```

### Upload Endpoint
```python
@app.post("/recipes/{recipe_id}/image")
def upload_recipe_image(...)
```

**Process:**
1. Receives file
2. Uploads to Cloudinary
3. Saves returned `secure_url` into DB

---

## 📤 Bulk Image Upload Script

To upload local images and generate Cloudinary URLs:

### upload_images.py
```python
for filename in os.listdir("assets"):
    result = cloudinary.uploader.upload(path, folder="recipe_vault")
    print(filename, result["secure_url"])
```

**Run:**
```bash
python upload_images.py
```

Then paste URLs into seed data.

---

## 🌱 Database Seeding

On startup, the API seeds the database with initial recipes and ingredients.

**Nested models are unpacked and mapped properly:**
- Recipe fields inserted into `recipes`
- Ingredients inserted into `ingredients`
- Enum values are converted to strings
- JSON instructions stored correctly

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recipes` | Get all recipes |
| GET | `/recipes/{id}` | Get recipe by id |
| POST | `/recipes` | Create recipe |
| PUT | `/recipes/{id}` | Update recipe |
| DELETE | `/recipes/{id}` | Delete recipe |
| POST | `/recipes/{id}/image` | Upload image |

---

## 🔄 ID Handling

- Database auto-generates IDs
- Schemas accept IDs only for reference
- CRUD operations use path parameters

**Example:**
```
PUT /recipes/12
DELETE /recipes/12
```

---

## ⚙️ Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/recipevault

CLOUDINARY_CLOUD_NAME=xxxx
CLOUDINARY_API_KEY=xxxx
CLOUDINARY_API_SECRET=xxxx
```

---

## ▶️ Run Locally

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start server
```bash
uvicorn main:app --reload
```

### Visit:
```
http://localhost:8000/docs
```

---

## 🧠 Key Concepts Learned

- Nested Pydantic models
- SQLAlchemy relationships
- Enum validation
- JSON fields in PostgreSQL
- File uploads with FastAPI
- Cloud storage integration
- Data seeding strategies
- Frontend-backend contract alignment

---

## 📈 Future Improvements

- [ ] Authentication (JWT)
- [ ] Pagination & filtering
- [ ] Recipe search
- [ ] User accounts
- [ ] Favorites
- [ ] Ratings system
- [ ] Migration with Alembic

---

## 🙌 Author

**Gaji Yaqub Ayomikun**  
Computer Science Student – LASU  
Backend Developer | Python | FastAPI

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

## ⭐ Show your support

Give a ⭐️ if this project helped you!
