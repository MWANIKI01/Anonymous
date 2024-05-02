
from dataclasses import Field
from wtforms import Form, StringField, TextAreaField, SubmitField, EmailField, ValidationError, FormField
from wtforms.validators import DataRequired, Email
from wtforms import widgets

class EmailForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Email()])

class AnonymousEmailForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = Field('Email', form_class=EmailForm, widget=EmailField())
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message')
    send = SubmitField('Send Email')
    
    @staticmethod
    def generate_temp_email():
        import requests

        # Make a request to 10minutemail.com to get a new email address
        response = requests.get('https://10minutemail.com/api/v1/')
        json_data = response.json()

        # Extract the email address from the JSON response
        temp_email = json_data['mail']

        return temp_email