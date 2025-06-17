import smtplib
import imghdr
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

password = os.getenv("EMAIL_PASSWORD")
sender = os.getenv("EMAIL_SENDER")
receiver = os.getenv("EMAIL_RECEIVER")

def send_email(image_path):
    print("se start")
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey we just saw a new customer")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()
    print("se end")

if __name__ == "__main__":
    send_email("images/sample.png")  # Optional test
