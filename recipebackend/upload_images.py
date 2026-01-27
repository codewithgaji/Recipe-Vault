import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv


load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


ASSETS_DIR = "assets"

# Create script to get the urls


for filename in os.listdir(ASSETS_DIR):
  path = os.path.join(ASSETS_DIR, filename)
  if not os.path.isfile(path):
    continue
  
  result = cloudinary.uploader.upload(path, folder="recipe_vault") # upload to Cloudinary
  print(filename, "=>", result["secure_url"])