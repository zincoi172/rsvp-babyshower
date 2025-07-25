from flask import Flask, render_template, request
import csv
from datetime import datetime
import smtplib
import os
import json
from email.message import EmailMessage
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("form.html")

@app.route('/submit', methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    attendance = request.form["attendance"]
    guests = request.form["guests"]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to CSV
    with open("responses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, email, attendance, guests])

    # Send confirmation email
    send_email(name, email, attendance, guests)

    # Log to Google Sheets
    log_to_google_sheets(name, email, attendance, guests)

    return render_template("thank_you.html", name=name)

def send_email(name, recipient, attendance, guests):
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = "RSVP Confirmation - Jubilee's Baby Shower"
    msg['From'] = email_address
    msg['To'] = recipient

    msg.set_content(f"""
    Hi {name},

    Thank you for your RSVP!

    Attendance: {attendance}
    Number of guests (including you): {guests}

    We look forward to celebrating with you!

    🧸 Jubilee Thiên Hân Tôn’s Baby Shower
    📍 2060 Mandelay Pl, San Jose, CA 95138
    📅 August 16, 2025 at 6:00 PM
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
            print("✅ Confirmation email sent.")
    except Exception as e:
        print("❌ Error sending email:", e)

def log_to_google_sheets(name, email, attendance, guests):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_json = os.getenv("GOOGLE_CREDS_JSON")
    if not creds_json:
        print("❌ GOOGLE_CREDS_JSON not set")
        return

    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open("RSVP Guest List").sheet1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([timestamp, name, email, attendance, guests])

if __name__ == '__main__':
    app.run(debug=True)
