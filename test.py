import unittest
import flask
from flask import Flask
import shg_app
import os
from app.models import Member, User, Shg, shg_meeting, member_meeting
from app.forms import RegistrationForm, SHGForm
from app import app, db
from app.forms import SHGForm


class TestSHGApp(unittest.TestCase):

    def setUp(self) -> None:
        db.create_all()
        reg_form1 = RegistrationForm
        reg_form1.username = 'jack'
        reg_form1.email = 'jack@gmail.com'
        reg_form1.password = 'jack123'
        reg_form1.confirm_password = 'jack123'
        self.u1 = User(username = reg_form1.username, email=reg_form1.email, password=reg_form1.password)
        reg_form2 = RegistrationForm
        reg_form2.username = 'mohandas'
        reg_form2.email = 'mohandas@gmail.com'
        reg_form2.password = 'mohan123'
        reg_form2.confirm_password = 'mohan123'
        self.u2 = User(username=reg_form2.username, email=reg_form2.email, password=reg_form2.password)
        # shg_form1 = SHGForm
        # self.s2 = Shg(name='maya shg', address='pilot colony', date_formed='1/2/2018', bank='SNC', branch='kaithal',
        #               account_num=4523453451333, saving_amt=150, user_id=2, num_members=12, total_savings=50000,
        #               expected_savings=60000)
        # self.s1 = Shg(name='krupa shg', address='pilot colony', date_formed='12/12/2018', bank='PNB', branch='kaithal',
        #               account_num=45234534513451, saving_amt=100, user_id=1, num_members=2, total_savings=5000,
        #               expected_savings=0)
        self.m1 = Member(name='Jeevan', gender='male', spouse_father='ram', age=25, soc_category='obc',
                         religion='hindu',
                         disability='no', apl='apl', outstanding_loan=2000, shg_id=1)
        self.m2 = Member(name='Ganga', gender='female', spouse_father='mohan', age=35, soc_category='sc',
                         religion='hindu',
                         disability='no', apl='bpl', outstanding_loan=1000, shg_id=2)
        self.m3 = Member(name='Nilofar', gender='female', spouse_father='fawad', age=27, soc_category='st',
                         religion='muslim',
                         disability='no', apl='apl', outstanding_loan=500, shg_id=1)
        self.m4 = Member(name='Neha', gender='female', spouse_father='aditya', age=41, soc_category='general',
                         religion='hindu', disability='yes', apl='bpl', outstanding_loan=0, shg_id=2)
        # self.smeet1 = shg_meeting(date='4/9/17', attendance=4, shg_id=1)
        # self.smeet2 = shg_meeting(date='14/5/17', attendance=8, shg_id=2)
        # self.mmeet1 = member_meeting(date='23/10/2014', attended='yes', amt_paid=100, bank_visits=1, govt_visits=0,
        #                              debt='no', loan_taken=0, loan_repaid=0, member_id=1)
        db.session.add(self.u1)
        db.session.add(self.u2)
        # db.session.add(self.s1)
        # db.session.add(self.s2)
        db.session.add(self.m1)
        db.session.add(self.m2)
        db.session.add(self.m3)
        db.session.add(self.m4)
        # db.session.add(self.smeet1)
        # db.session.add(self.smeet2)
        # db.session.add(self.mmeet1)

        db.session.commit()

    def tearDown(self) -> None:
        db.session.delete(self.u1)
        db.session.delete(self.u2)
        # db.session.delete(self.s1)
        # db.session.delete(self.s2)
        db.session.delete(self.m1)
        db.session.delete(self.m2)
        db.session.delete(self.m3)
        db.session.delete(self.m4)
        # db.session.delete(self.smeet1)
        # db.session.delete(self.smeet2)
        # db.session.delete(self.mmeet1)
        db.session.commit()

    def test_user_form(self):
        self.assertEqual(self.u1.username, 'jack')
        self.assertEqual(self.u1.email, 'jack@gmail.com')
        self.assertEqual(self.u1.password, 'jack123')
        self.assertEqual(self.u2.username, 'mohandas')
        self.assertEqual(self.u2.email, 'mohandas@gmail.com')
        self.assertEqual(self.u2.password, 'mohan123')

    # def test_shg_form(self):
    #     self.assertEqual(self.s1.expected_savings, 0)
    #     self.assertEqual(self.s1.date_formed, '12/12/2018')
    #     self.assertEqual(self.s2.date_formed, '1/2/2018')

    def test_member_form(self):
        self.assertEqual(self.m1.soc_category, "obc")
        self.assertEqual(self.m1.gender, 'male')
        self.assertEqual(self.m1.outstanding_loan, 2000)
        self.assertEqual(self.m2.apl, 'bpl')
        self.assertEqual(self.m2.shg_id, 2)
        self.assertEqual(self.m2.religion, 'hindu')

    # def test_shg_meeting_form(self):
    #     self.assertEqual(self.smeet1.attendance, 4)
    #     self.assertEqual(self.smeet1.date, '4/9/17')
    #     self.assertEqual(self.smeet2.date, '14/5/17')
    #
    # def test_member_meeting_form(self):
    #     self.assertEqual(self.mmeet1.date, '23/10/2014')

    def test_db_user(self):
        users = User.query.all()
        print(users)


if __name__ == '__main__':
    unittest.main()
