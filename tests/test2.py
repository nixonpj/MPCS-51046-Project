from app import db
from app.models import User, Shg, Member
from app.forms import SHGForm
from datetime import datetime
db.create_all()
users = User.query.all()
members = Member.query.all()
shgs = Shg.query.all()
u1 = User(username='jeet', email='j@g.com', password='password')
u2 = User(username='bhupen', email='bhups@g.com', password='password1')
u3 = User(username='zorawar', email='zor@g.com', password='password2')
s1 = Shg(name='megha', address='odisha', date_formed=datetime(2013, 2, 2), bank='SBI', branch='Delhi', account_num=433567353453,
         saving_amt=100, user_id=u1.id, num_members=0, total_savings=20000,
         expected_savings=SHGForm.expected_savings(datetime('1-4-2018'), 100))
s2 = Shg(name='heeran', address='punjab', date_formed=datetime('10-7-2018'), bank='PNB', branch='Delhi', account_num=22356733453,
         saving_amt=150, user_id=u1.id, num_members=0, total_savings=10000,
         expected_savings=SHGForm.expected_savings(datetime('10-7-2018'), 150))
s3 = Shg(name='dweep', address='kerala', date_formed=datetime('1-4-2017'), bank='OBC', branch='Delhi', account_num=111567353453,
         saving_amt=120, user_id=u2.id, num_members=0, total_savings=15000,
         expected_savings=SHGForm.expected_savings(datetime('1-4-2017'), 120))
s4 = Shg(name='bhakti', address='haryana', date_formed=datetime('11-2-2017'), bank='ANC', branch='Delhi', account_num=111567353453,
         saving_amt=150, user_id=u2.id, num_members=0, total_savings=17000,
         expected_savings=SHGForm.expected_savings(datetime('11-2-2017'), 150))
s5 = Shg(name='maya', address='uttarakhand', date_formed=datetime('1-4-2017'), bank='BOB', branch='Delhi', account_num=111567353453,
         saving_amt=200, user_id=u3.id, num_members=0, total_savings=19000,
         expected_savings=SHGForm.expected_savings(datetime('1-4-2017'), 200))
# m1 = Member(name=form.name.data, gender=form.gender.data, spouse_father=form.spouse_father.data,
#                         age=form.age.data, soc_category=form.soc_category.data, religion=form.religion.data,
#                         disability=form.disability.data, apl=form.apl.data,
#                         total_saving=0, outstanding_loan=form.outstanding_loan.data, shg_id=shg_id)

