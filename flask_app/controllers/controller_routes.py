from flask import flash, render_template, redirect, request
from flask_app import app
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import os

#landing page
@app.route('/')
def landing_page():
    return render_template("index.html")

@app.route('/events')
def events_page():
    return render_template("events.html")

@app.route('/history')
def history_page():
    return render_template("history.html")

@app.route('/gallery')
def gallery_page():
    # gallery_folder = '/home/jessethommes/AcclaimedCC/flask_app/static/imgs/gallery'
    gallery_folder = 'flask_app\static\imgs\gallery'
    images = os.listdir(gallery_folder)
    return render_template("gallery.html",images=images)

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route('/private')
def private_page():
    return render_template("private.html")

@app.route('/submit', methods=["post"])
def submit():
    data = request.form

    email_sender = 'requestformreply@gmail.com'
    email_password = 'kulp dmej mpko nswu'
    email_reciever = 'jthommes22@gmail.com'#TODO change email
    sender_display_name = 'Willmar Whisky Society'#displays as email sender

    subject = f'{data["name"]} would like more information'
    body = f"""
    <html>
    <body>
        <p><b>{data['name']}</b> would like more information:</p>
        <p>{data['comments']}</p>
        <p><b>Name:</b> {data['name']}</p>
        <p><b>Email:</b> {data['email']}</p>
        <p><b>Phone Number:</b> {data['phone']}</p>
        <p><b>City:</b> {data['city']}</p>
    </body>
    </html>
    """

    em = MIMEMultipart('alternative')
    em['From'] = f'{sender_display_name} <{email_sender}>'
    em['To'] = email_reciever
    em['Subject'] = subject
    # em.set_content(body)

    em.add_header('Reply-To', data['email'])

    em.attach(MIMEText(body, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_reciever,em.as_string())
        flash("MESSAGE SENT! Thank you for your interest in Willmar Whiskey Society!")

    return redirect('/contact')

# email tutorial
# https://www.youtube.com/watch?v=g_j6ILT-X0k
# log into google account
# url.. myaccount.google.com/u/4/?tab=kk
# url.. myaccount.google.com/u/4/apppasswords