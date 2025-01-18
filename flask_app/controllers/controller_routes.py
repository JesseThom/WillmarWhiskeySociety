from flask import flash, render_template, redirect, request, session
from flask_app import app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from PIL import Image
from datetime import datetime
import urllib.parse
# from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import os

from flask_app.models.model_users import User
from flask_app.models.model_events import Event

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#landing page
@app.route('/')
def landing_page():
    return render_template("index.html")

@app.route('/events')
def events_page():
    events = Event.get_all_current()
    return render_template("events.html",events=events)

@app.route('/details/<int:id>')
def details(id):
    event = Event.get_one_by_id({'id':id})

    # URL-encode the address
    encoded_address = urllib.parse.quote(event.address)
    # Create the Google Maps URL
    google_maps_url = f"https://www.google.com/maps?q={encoded_address}&output=embed"

    return render_template('details.html',event=event, google_maps_url=google_maps_url)

@app.route('/history')
def history_page():
    events = Event.get_all_history()
    return render_template("history.html",events=events)

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route('/private')
def private_page():
    return render_template("private.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/submit_admin', methods=['POST'])
def submit_admin():
    data = request.form
    user = User.get_one_by_name({'name':data['name']})

    if not User.validate_login(data,user):
        return redirect('/login')
    
    session['uuid'] = user.id

    return redirect("/admin")

@app.route('/admin')
def admin():
    if 'uuid' not in session:
        return redirect('/login')
    
    events = Event.get_all()

    return render_template("admin.html",events=events)

@app.route('/add_event')
def add_event():
    if 'uuid' not in session:
        return redirect('/login')

    today =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('add_event.html',today=today)

@app.route('/create_event', methods=['POST'])
def create_event():
    
    # check for existing id#
    temp = Event.get_one_by_id({'id':request.form['id']})
    if temp:
        flash("Event Id Exists", 'err_id')
        return render_template("add_event.html")
    
    # img processing
    file = request.files['pic_location']

    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER,file.filename)
        rgb_image = Image.open(file).convert('RGB')
        rgb_image.save(file_path)

        data ={
            **request.form,
            'pic_location':file.filename,
        }

        Event.create(data)
        flash("Event Created", 'err_created')
        return redirect('/admin')
    else:
        flash("Invalid file format", 'err_file')
        return render_template("add_event.html")

@app.route('/edit_event/<int:id>')
def edit_event(id):
    if 'uuid' not in session:
        return redirect('/login')
    
    event = Event.get_one_by_id({'id':id})
    file_path = os.path.join(UPLOAD_FOLDER,event.pic_location)
    return render_template('edit_event.html',event=event,file_path=file_path)

@app.route('/update_event', methods=['POST'])
def update_event():
    # move to history page
    if not request.form.get('history'):
        history = 0
    else:
        history = 1

    # img processing
    file = request.files['pic_location']

    if file and allowed_file(file.filename):
        # save new img
        file_path = os.path.join(UPLOAD_FOLDER,file.filename)
        rgb_image = Image.open(file).convert('RGB')
        rgb_image.save(file_path)

        # remove old img
        image_filename = request.form['pic_location']
        if image_filename:
            file_path = os.path.join(UPLOAD_FOLDER, image_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print("file deleted")

        data ={
            **request.form,
            'pic_location':file.filename,
            'history':history
        }

    else:
        data = {
            **request.form,
            'history':history
        }


    Event.update_one(data)
    return redirect('admin')

@app.route('/delete_event/<int:id>')
def delete_event(id):
    if 'uuid' not in session:
        return redirect('/login')

    # delete img
    event = Event.get_one_by_id({'id':id})
    if event:
        image_filename = event.pic_location
        if image_filename:
            file_path = os.path.join(UPLOAD_FOLDER, image_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print("file deleted")

    Event.delete_one({'id':id})
    return redirect("/admin")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")


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
        <p>{data['message']}</p>
        <p><b>Name:</b> {data['name']}</p>
        <p><b>Email:</b> {data['email']}</p>
    </body>
    </html>
    """

    em = MIMEMultipart('alternative')
    em['From'] = f'{sender_display_name} <{email_sender}>'
    em['To'] = email_reciever
    em['Subject'] = subject

    em.add_header('Reply-To', data['email'])

    em.attach(MIMEText(body, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_reciever,em.as_string())
        flash("MESSAGE SENT! Thank you for your interest in Willmar Whiskey Society!", 'err_sent')

    return redirect('/contact')

# email tutorial
# https://www.youtube.com/watch?v=g_j6ILT-X0k
# log into google account
# url.. myaccount.google.com/u/4/?tab=kk
# url.. myaccount.google.com/u/4/apppasswords