
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class GreetUserForm(FlaskForm):
    itemName = StringField(label=('Enter Your Name:'))
    submit = SubmitField(label=('Submit'))