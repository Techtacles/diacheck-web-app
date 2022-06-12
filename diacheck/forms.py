from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, IntegerField,BooleanField,SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp,Optional
from flask_login import current_user
from diacheck.models import User

#User Forms

class RegistrationForm(FlaskForm):
    first_name = StringField('Firstname', render_kw={'placeholder':'First Name'}, validators=[DataRequired(), Length(1,100), 
                                                  Regexp(r"^[a-zA-Z_.-]+$", 0, 'Firstname must have only letters, dots , underscores and hyphen')])
    last_name = StringField('Lastname', render_kw={'placeholder':'Last Name'}, validators=[DataRequired(), Length(1,100), 
                                                  Regexp(r"^[a-zA-Z_.-]+$", 0, 'Lastname must have only letters, dots , underscores and hyphen')])
    email = StringField('Email', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

