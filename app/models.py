from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

"""
This module contains all the tables to be stored in the database. 
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Creates a db Model for Users who register and login
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    shgs = db.relationship('Shg', backref='coordinator', lazy=True)

    def __repr__(self):
        return f'User {self.username}'


# class Coop(db.Model, UserMixin):
#     """
#     Creates a db Model for Cooperatives
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     date_formed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     address = db.Column(db.String(120), index=True)
#     bank = db.Column(db.String(30), index=True)
#     branch = db.Column(db.String(30), index=True)
#     account_num = db.Column(db.Integer)
#     saving_amt = db.Column(db.Integer, index=True, default=100)
#     shgs = db.relationship('Shg', backref='coop', lazy=True)
#     total_savings = db.Column(db.Integer)
#
#     def __repr__(self):
#         return f'User {self.name}'


class Shg(db.Model, UserMixin):
    """
    Creates a db Model for Self help groups. Linked to Users by user_id.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_formed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    address = db.Column(db.String(120), index=True)
    bank = db.Column(db.String(30), index=True)
    branch = db.Column(db.String(30), index=True)
    saving_amt = db.Column(db.Integer, index=True, default=100)
    account_num = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_savings = db.Column(db.Integer)
    expected_savings = db.Column(db.Integer)
    members = db.relationship('Member', backref='shg', lazy=True)
    meetings = db.relationship('shg_meeting', backref='shg', lazy=True)
    num_members = db.Column(db.Integer)
    # coop_id = db.Column(db.Integer, db.ForeignKey('coop.id'), nullable=True)

    def __repr__(self):
        return f"SHG('{self.name}', '{self.date_formed}')"


class Member(db.Model, UserMixin):
    """
    Creates a Member db model for individual members of a SHG. Linked to SHGs by shg_id.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String)
    spouse_father = db.Column(db.String)
    age = db.Column(db.Integer)
    religion = db.Column(db.String)
    soc_category = db.Column(db.String)
    disability = db.Column(db.String)
    apl = db.Column(db.String)
    total_saving = db.Column(db.Integer)
    outstanding_loan = db.Column(db.Integer)
    meeting = db.relationship('member_meeting', backref='member', lazy=True)
    shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)

    def __repr__(self):
        return f"SHG Member {self.name}"


class shg_meeting(db.Model, UserMixin):
    """
    Creates a db model for shg meeting. Only storing date and total attendance.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    attendance = db.Column(db.Integer)
    shg_id = db.Column(db.Integer, db.ForeignKey('shg.id'), nullable=False)


class member_meeting(db.Model, UserMixin):
    """
    Creates a db model storing information about individual SHG members at meetings.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    attended = db.Column(db.String)
    amt_paid = db.Column(db.Integer)
    bank_visits = db.Column(db.Integer)
    govt_visits = db.Column(db.Integer)
    debt = db.Column(db.String)
    loan_taken = db.Column(db.Integer)
    loan_repaid = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)














