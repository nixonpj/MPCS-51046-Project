from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User
from datetime import date

"""
This module creates forms using flask_wtf. Each form takes in the attributes as required by the database models that 
are created in the models module. These forms are imported in the routes module and then rendered using Jinja2.
"""


class RegistrationForm(FlaskForm):
    """
    Creates a Flaskform that takes in username, email and password from the user db model in models.py.
    Validates when clicked on submit. Also checks if username and email already exists.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    Takes in email and password. Option to remember the user.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SHGForm(FlaskForm):
    """
    Creates a FlaskForm that takes in all attributes that are required for the SHG Model from models.
    Expected savings calculated separately based on given inputs.
    """
    # def coops_populate():
    #     coops = Coop.query.all()
    #     if len(list(coops)) == 0:
    #         return [('none', 'None')]
    #     coops_list = [(coop.name, str.lower(coop.name)) for coop in coops]
    #     return coops_list

    @staticmethod
    def expected_savings(date_formed, saving_amt):
        time_now = date.today()
        age_months = int((time_now - date_formed).days / 30)
        return age_months * saving_amt

    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(5, 30)])
    saving_amt = IntegerField('Saving Amount', validators=[DataRequired(), NumberRange(10, 200)])
    date_formed = DateField('Date of Formation', format='%d/%m/%Y', default=date.today)
    account_num = IntegerField('Account Number:', validators=[DataRequired()])
    bank = StringField('Bank Name', validators=[DataRequired()])
    branch = StringField('Branch Name:', validators=[DataRequired()])
    total_savings = IntegerField('Total Savings(₹)', validators=[DataRequired(), NumberRange(0, 1000000)])
    # coop = SelectField('Cooperative Name', choices=coops_populate())
    submit = SubmitField('Update')


class MemberForm(FlaskForm):
    """
    Creates a Flaskform that takes in all the attributes from the Member Model from models.py
    """
    name = StringField('Name', validators=[DataRequired(), Length(3, 30)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    spouse_father = StringField('Name of Father/Spouse', validators=[DataRequired(), Length(3, 30)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(16, 99)])
    religion = SelectField('Religion', choices=[('hindu', 'Hindu'), ('muslim', 'Muslim'), ('sikh', 'Sikh'),
                                                ('christian', 'Christian'), ('buddhist', 'Buddhist'), ('jain', 'Jain'),
                                                ('other', 'Other')])
    soc_category = SelectField('Social/Caste Category', choices=[('general', 'General'), ('obc', 'OBC'), ('sc', 'SC'),
                                                                 ('st', 'ST'), ('other', 'Other')])
    disability = SelectField('Disability', choices=[('yes', 'Yes'), ('no', 'No')])
    apl = SelectField('Poverty Category', choices=[('apl', 'APL'), ('bpl', 'BPL'), ('antyodaya', 'Antyodaya')])
    # total_saving = IntegerField('Total Savings(₹)', validators=[DataRequired(), NumberRange(0, 1000000)])
    outstanding_loan = IntegerField('Total Outstanding Loan(₹)', validators=[NumberRange(0, 100000)])
    submit = SubmitField('Update')


class SHGMeetingForm(FlaskForm):
    """
    Creates a Flaskform that takes in all the attributes from the SHG Meeting Model from models.py
    """
    date = DateField('Date of Meeting', format='%d/%m/%Y', default=date.today())
    # attendance = IntegerField('Attendance', validators=[DataRequired()])
    submit = SubmitField('Update')


class MemberMeetingForm(FlaskForm):
    """
    Creates a Flaskform that takes in all the attributes from the Member Meeting Model from models.py
    """
    date = DateField('Date of Meeting', format='%d/%m/%Y', default=date.today())
    attended = SelectField('Attendance', choices=[('present', 'Present'), ('absent', 'Absent')])
    bank_visits = IntegerField('Bank Visits last month', validators=[DataRequired(), NumberRange(0, 9)])
    govt_visits = IntegerField('Govt. Office Visits last month', validators=[DataRequired(), NumberRange(0, 9)])
    amt_paid = IntegerField('Amount Paid', validators=[DataRequired(), NumberRange(0, 999)])
    debt = SelectField('Previous Debt', choices=[('yes', 'Yes'), ('no', 'No')])
    loan_taken = IntegerField('Loan Taken', validators=[DataRequired(), NumberRange(0, 9999)])
    loan_repaid = IntegerField('Loan Repaid', validators=[DataRequired(), NumberRange(0, 9999)])
    submit = SubmitField('Update')
