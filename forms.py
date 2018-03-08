from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

class CreateAccount(FlaskForm):
    firstname = StringField('FIRST NAME', validators=[DataRequired(), Length(min=1, max=50)])
    middlename = StringField('MIDDLE NAME', validators=[DataRequired(), Length(min=1, max=50)])
    lastname = StringField('LAST NAME', validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('USERNAME', validators=[DataRequired(), Length(min=4, max=25)])
    # password = PasswordField('PASSWORD', validators=[DataRequired(), Length(min=6, max=32)])
    # repeatpass = PasswordField('REPEAT PASSWORD', validators=[DataRequired(), EqualTo('password', message="Password must MATCH")])
    # officerrole = StringField('Officer Type of Role', validators=[DataRequired(), Length(min=3, max=50)])