import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content(
    "Test"
)
try:
    
    msg["Subject"] = f"Installed software list"
    msg["From"] = "YourSenderEmailn@gmail.com"
    msg["To"] = "YourReceive@gmail.com" 
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("SenderEmail@gmail.com", "Your API Key")
    server.send_message(msg)
    server.quit()
    print("-" * 20, "Email Send Success ", "-" * 20)

    del msg["Subject"] # Clear the value
    del msg["From"] # Clear the value
    del msg["To"]  # Clear the value
except:
    print(f"Error: Email Send failed")
    
