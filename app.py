from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, SubmitField, validators
from wtforms.validators import Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import faker  # type: ignore
import os
import base64
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = base64.b64encode(os.urandom(32)).decode()
app.config['STATIC_FOLDER'] = 'static'

load_dotenv()  # Load environment variables from .env file

email_address = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

class AnonymousEmailForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    subject = StringField('Subject', validators=[validators.DataRequired()])
    message = TextAreaField('Message')
    send = SubmitField('Send Email')

@app.route('/')
def index():
    form = AnonymousEmailForm()
    return render_template('index.html', form=form)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.route('/send', methods=['POST'])
def send_email():
    form = AnonymousEmailForm(request.form)
    if form.validate():
        receiver_email = form.email.data

        message = MIMEMultipart()
        message['From'] = email_address
        message['To'] = receiver_email
        message['Subject'] = form.subject.data

        body = f"{form.name.data}\n\n{form.message.data}"
        message.attach(MIMEText(body, 'plain'))

        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(email_address, password)
            smtp_server.sendmail(email_address, receiver_email, message.as_string())
            smtp_server.quit()
            flash('Email sent successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(str(e))
            flash('Failed to send email. Please check your email address and try again.', 'error')
    else:
        flash('Invalid input, please check your details and try again.', 'error')
        return redirect(url_for('index'))

def generate_temp_email():
    fake = faker.Faker()
    first_name, last_name = fake.name().split()
    email = f"{first_name}.{last_name}@temp-mail.org"
    return email

if __name__ == '__main__':
    app.run(debug=True)