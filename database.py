import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/database.db"
db = SQLAlchemy(app)

#You can create a basic model for your user or email data:

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    messages = db.relationship('Message', backref='sender', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#Now, you can create, retrieve, update, and delete records from the database using SQLAlchemy and Flask. For example, you can create a new user and a message for that user:

new_user = User(email="test@test.com", name="Test User")
db.session.add(new_user)
db.session.commit()

new_message = Message(
    sender=new_user,
    recipient_email="recipient@example.com",
    subject="Hello there",
    message="This is a test message!",
)
db.session.add(new_message)
db.session.commit()

#To view all records in the database, you can use the following command:

users = User.query.all()
for user in users:
    print(f"User: {user.name} ({user.email})")
    messages = user.messages
    for message in messages:
        print(f"\tMessage to: {message.recipient_email}")
        print(f"\tSubject: {message.subject}")
        print(f"\tMessage: {message.message}")
        print("\tTimestamp: " + str(message.timestamp))