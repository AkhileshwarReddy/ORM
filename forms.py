from flask import url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, BooleanField, PasswordField, SelectMultipleField, SubmitField, TextAreaField, SelectField, IntegerField, FormField
from utilities import *
from wtforms.fields.html5 import DateField, URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
import re

class LoginForm(FlaskForm):
    user = StringField('Username',validators = [DataRequired(), Length(min=4,max=20)])
    password = PasswordField('Password',validators = [DataRequired(),Length(min=6)])
    remember = BooleanField()
    submit = SubmitField('Login')

    def validate_user(form,user):
        from app import User
        if not User.query.filter_by(user=user.data).first():
            raise ValidationError("Username Invalid")
    

class SignUpForm(FlaskForm):
    user = StringField('Username',validators = [DataRequired(), Length(min=4,max=20)])
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password',validators = [DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password',message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_user(form, user):
        from app import User
        if not re.search("\W",user.data):
            if User.query.filter_by(user = user.data).first():
                raise ValidationError("Username already taken. Choose Another One.")
        else:
            raise ValidationError("Username should not contain special symbols except underscore.")

    def validate_email(form,email):
        from app import User
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email Already Exists.")
    
class EducationForm(Form):
    instituteName = StringField('Institute Name',validators=[DataRequired(),Length(min=5,max=50)])
    joiningYear = SelectField('Joining Year',validators=[DataRequired()],choices = academYearsList(1970,2021,1))
    passOutYear = SelectField('Passout Year',validators=[DataRequired()],choices = academYearsList(1970,2021,0))
    instituteAddress = StringField('Institute Address',validators=[DataRequired(),Length(max=50)])
    score = StringField('Academic Score',validators=[DataRequired(),Length(min=2,max=5)])

class AcademicForm(FlaskForm):
    ssc = FormField(EducationForm)
    diporint = SelectField('Diploma or Intermediate',validators=[DataRequired()],choices=[(None,'Select your Choice'),('Diploma','Diploma'),('Intermediate','Intermediate')])
    dip_int = FormField(EducationForm)
    ug_stream = SelectField('UG Stream',validators=[DataRequired()],choices=[(None,'Select Stream'),("B.E/B.Tech","B.E/B.Tech")])
    ug_branch = StringField('UG Branch',validators=[DataRequired()])
    ug = FormField(EducationForm)
    submit = SubmitField('Save & Submit')

class FeedBackForm(FlaskForm):
    name = StringField('Name',validators = [DataRequired(),Length(min=4,max=20)])
    email = StringField('Email',validators = [DataRequired(),Email()])
    select = SelectField('FeedBack Type',choices = [(None,'Message Type'),('bugs','Bugs'),('suggestions','Suggestions'),('questions','Questions')])
    message = TextAreaField('feedback')
    submit = SubmitField('Submit')

class ForgotPassword(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Reset Password')

    def validate_email(form,email):
        from app import User
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('There is no account with that email id.')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password',validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('new_password',message='Passwords Must Match')])
    submit = SubmitField('Reset Password')

class AddressForm(Form):
    state = SelectField('Select State',validators=[DataRequired()],choices=statesList)
    district = StringField('District',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    door_number = StringField('Door No',validators=[DataRequired()])
    pincode = StringField('Pincode',validators=[DataRequired()])

class UrlForm(Form):
    facebook = URLField('Facebook URL',validators=[Optional()])
    twitter = URLField('Twitter URL',validators=[Optional()])
    github = URLField('Github URL',validators=[Optional()])
    stack_overflow = URLField('Stack Overflow URL',validators=[Optional()])
    linkedin = URLField('LinkedIn URL',validators=[Optional()])

class ProjectsForm(Form):
    title = StringField('Title',validators=[Optional(),Length(min=4,max=30)])
    des = TextAreaField('Project Description',validators=[Optional(),Length(min=20,max=1000)])

class SkillForm(FlaskForm):
    soft_skills = SelectMultipleField('Soft Skills',validators=[Optional()],choices=softSkillsList)
    tech_skills = SelectMultipleField('Technical Skills',validators=[Optional()],choices=techSkillsList)
    langs_known = SelectMultipleField('Languages',validators=[Optional()],choices=[('English','English'),('Telugu','Telugu'),('Hindi','Hindi'),('Tamil','Tamil'),('Kannada','Kannada')])
    urls = FormField(UrlForm)
    submit = SubmitField('Save')

class PersonalInfoForm(FlaskForm):
    firstName = StringField('First Name',validators=[DataRequired(),Length(min=2,max=30)])
    middleName = StringField('Middle Name')
    lastName = StringField('Last Name',validators=[DataRequired(),Length(min=1,max=20)])
    dob = DateField('Date of Birth',validators=[DataRequired()],format='%Y-%m-%d')
    permanentAddress = FormField(AddressForm)
    currentAddress = FormField(AddressForm)
    emailPrimary = StringField('Primary Email',validators=[DataRequired(),Email(message="Invalid Email")])
    emailSecondary = StringField('Secondary Email',validators=[Optional(),Email(message="Invalid Email")])
    contactPrimary = StringField('Contact Primary',validators=[DataRequired()])
    contactSecondary = StringField('Contact Secondary',validators=[Optional()])
    description = TextAreaField("Description",validators=[DataRequired(),Length(min=200,max=1000)])
    submit = SubmitField('Save & Next')

class ExperienceForm(FlaskForm):
    company = StringField('Company',validators=[DataRequired()])
    experience = IntegerField('Experience',validators=[DataRequired()])
    position = StringField('Position',validators=[DataRequired(),Length(min=2,max=30)])
    submit = SubmitField('Save')
