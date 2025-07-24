from flask import Flask, render_template, request
import csv
from datetime import datetime
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("form.html")

@app.route('/submit', methods=["POST"])
def submit():
    name = request.form["name"]
    attendance = request.form["attendance"]
    guests = request.form["guests"]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to CSV
    with open("responses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, attendance, guests])

    # Send confirmation email
    send_email(name, attendance, guests)

    # Show thank-you page with confetti
    return render_template("thank_you.html")

def send_email(name, attendance, guests):
    email_address = "your_email@gmail.com"
    email_password = "your_app_password"  # Use App Password for Gmail
    recipient = "recipient_email@example.com"  # Can be dynamic if you collect user's email

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
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
            print("Confirmation email sent.")
    except Exception as e:
        print("Error sending email:", e)

if __name__ == '__main__':
    app.run(debug=True)
