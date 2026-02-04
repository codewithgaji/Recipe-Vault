import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv(r"C:\Users\Gaji\Documents\Recipe Vault\recipebackend\.env")

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")



if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
  raise ValueError("GMAIL_EMAIL or GMAIL_APP_PASSWORD not found in .env")

GMAIL_APP_PASSWORD = GMAIL_APP_PASSWORD.replace(" ", "")

msg = EmailMessage()

msg["Subject"] = "Testing For Testing Sake, lol"
msg["From"] = GMAIL_EMAIL
msg["To"] = "gajiyakub2@gmail.com"
msg.set_content("Hello Yk, \n\nI really Love seeing my Python Code being able to send a mail, Lol \n\nLet's Improve Okay, \nThanks")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
  smtp.ehlo()
  smtp.starttls()
  smtp.ehlo()
  smtp.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
  smtp.send_message(msg)

print("SENT SUCCESSFULLY")