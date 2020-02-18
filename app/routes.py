import os
from app import app, db  # ,bcrypt
from flask import render_template, flash, url_for, redirect, request
from app.forms import LoginForm, RegistrationForm, SHGForm, MemberForm, SHGMeetingForm, MemberMeetingForm
from app.models import User, Shg, Member, shg_meeting, member_meeting
from flask_login import login_user, current_user, logout_user, login_required

"""
This module imports forms from forms module and renders them using the templates in the templates directory.
The information from the forms as given by the user are then stored in the database if necessary. 
"""


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    landing page for beginners; takes inputs for RegistrationForm and if valid inputs are given stores the information
    in db. Thereafter redirects to login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Takes in inputs for the LoginForm and and if valid provides access to other pages.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/')
@app.route('/home')
def home():
    """
    Queries all available SHGs from db and displays them to the user.
    """
    shgs = Shg.query.all()
    return render_template('home.html', title='Home', shgs=shgs)


@app.route("/about")
def about():
    """
    Shows basic information about the app.
    """
    return render_template('about.html', title='About')


@app.route("/logout")
def logout():
    """
    Logouts the current user and redirects to login page.
    """
    logout_user()
    return redirect(url_for('login'))


@app.route("/account")
@login_required
def account():
    """
    Displays name of the user. Can build more information if required.
    """
    return render_template('account.html', title='Account')


@app.route("/shg/add", methods=['GET', 'POST'])
@login_required
def add_shg():
    """
    Displays the SHGForm and takes in input for each attribute. Valid submissions are saved in the db.
    Redirects to the home page after submission.
    """
    form = SHGForm()
    if form.validate_on_submit():
        # coop_name = form.coop.data
        # coops = 0
        # if coop_name != 'none':
        #     coops_list = Coop.query.all()
        #     for coop in coops_list:
        #         if coop.name == coop_name:
        #             coops = coop.id
        shg = Shg(name=form.name.data, address=form.address.data, date_formed=form.date_formed.data,
                  bank=form.bank.data, branch=form.branch.data, account_num=form.account_num.data,
                  saving_amt=form.saving_amt.data, user_id=current_user.id, num_members=0,
                  total_savings=form.total_savings.data,
                  expected_savings=form.expected_savings(form.date_formed.data, form.saving_amt.data))
        db.session.add(shg)
        db.session.commit()
        flash('SHG has been successfully added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_shg.html', title='New SHG', form=form, legend='New SHG')


@app.route("/shg/<int:shg_id>", methods=['GET', 'POST'])
def shg(shg_id):
    """
    The page displays the details of a given SHG including details of all members.
    :param shg_id: The SHG ID as stored in db of the shg whose details are to be displayed.
    """
    shg = Shg.query.get_or_404(shg_id)
    members = Member.query.filter_by(shg_id=shg.id)
    return render_template('shg.html', title=shg.name, shg=shg, members=members)


@app.route("/shg/<int:shg_id>/update", methods=['GET', 'POST'])
@login_required
def update_shg(shg_id):
    """
    Provides the SHGForm with pre-filled data. User can change any field and submit the new form.
    :param shg_id: The SHG ID as stored in db of the shg whose details are to be updated.
    :return: On submission redirects to the shg page.
    """
    shg = Shg.query.get_or_404(shg_id)
    # uncomment this section if you want the update functionality to be available only for the user who created the SHG
    # if shg.user_id != current_user.id:
    #     os.abort(403)
    form = SHGForm()
    if form.validate_on_submit():
        # shg.name = form.name.data
        # shg.address = form.address.data
        # shg.date_formed = form.date_formed.data
        shg.bank = form.bank.data
        shg.branch = form.branch.data
        shg.account_num = form.account_num.data
        shg.saving_amt = form.saving_amt.data
        shg.total_savings = form.total_savings.data
        # shg.user_id = current_user.id
        shg.expected_savings = form.expected_savings(form.date_formed.data, form.saving_amt.data)
        db.session.commit()
        flash('SHG has been updated!', 'success')
        return redirect(url_for('shg', shg_id=shg.id))
    elif request.method == 'GET':
        form.name.data = shg.name
        form.address.data = shg.address
        form.saving_amt.data = shg.saving_amt
        form.date_formed.data = shg.date_formed
        form.account_num.data = shg.account_num
        form.bank.data = shg.bank
        form.branch.data = shg.branch
        form.total_savings.data = shg.total_savings
    return render_template('add_shg.html', title='Update SHG',
                           form=form, legend='Update SHG')


@app.route("/shg/<int:shg_id>/delete", methods=['POST'])
@login_required
def delete_shg(shg_id):
    """
    The shg data related to the given shg_id is deleted from the db
    :param shg_id: The SHG ID as stored in db of the shg whose details are to be deleted from the db.
    :return: Redirected to the home page
    """
    shg = Shg.query.get_or_404(shg_id)
    if shg.user_id != current_user.id:
        os.abort(403)
    db.session.delete(shg)
    db.session.commit()
    flash('SHG has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/shg/<int:shg_id>/member/add", methods=['GET', 'POST'])
@login_required
def add_member(shg_id):
    """
    Displays and takes input for the MemberForm. Each attribute for an individual SHG member is received and finally
    stored. The member created is a part of a SHG given by shg_id.
    Increase the count of shg.members attribute for each member created.
    Also distribute the total savings of the SHG amongst all members of SHG after incrementing number of SHG members.
    :param shg_id: The SHG ID of the shg in which a member is to be added.
    :return: On valid submission, redirects to the shg page.
    """
    shg = Shg.query.get_or_404(shg_id)
    form = MemberForm()
    if form.validate_on_submit():
        member = Member(name=form.name.data, gender=form.gender.data, spouse_father=form.spouse_father.data,
                        age=form.age.data, soc_category=form.soc_category.data, religion=form.religion.data,
                        disability=form.disability.data, apl=form.apl.data, total_saving=0,
                        outstanding_loan=form.outstanding_loan.data, shg_id=shg_id)
        db.session.add(member)
        db.session.commit()
        member.shg.num_members += 1
        db.session.commit()
        for each_member in shg.members:
            each_member.total_saving = int(shg.total_savings / shg.num_members)
        db.session.commit()
        flash('Member has been successfully added!', 'success')
        return redirect(url_for('shg', shg_id=shg.id))
    return render_template('add_update_member.html', title='New SHG Member', form=form, legend='New SHG Member')


@app.route("/shg/<int:shg_id>/member/<int:member_id>", methods=['GET', 'POST'])
@login_required
def member(shg_id, member_id):
    """
    Queries given member id and then displays all the attributes.
    :param shg_id: Input SHG ID stored in db of the shg whose member's details are to be displayed.
    :param member_id: Input Member ID stored in db of the shg member whose details are to be displayed.
    """
    member = Member.query.get_or_404(member_id)
    return render_template('member.html', title='Member Details', shg_id=shg_id, member=member)


@app.route("/shg/<int:shg_id>/member/<int:member_id>/update", methods=['GET', 'POST'])
@login_required
def update_member(shg_id, member_id):
    """
    Takes the member form and prefills it with available data. User can edit any field and the changes will be saved
    to the database.
    :param shg_id: Input SHG ID stored in db of the shg whose member's details are to be updated.
    :param member_id: Input Member ID stored in db of the shg member whose details are to be updated.
    :return: Redirects to SHG Member Page on valid submission.
    """
    shg = Shg.query.get_or_404(shg_id)
    member = Member.query.get_or_404(member_id)
    if shg.user_id != current_user.id:
        os.abort(403)
    form = MemberForm()
    if form.validate_on_submit():
        member.name = form.name.data
        member.spouse_father = form.spouse_father.data
        member.gender = form.gender.data
        member.outstanding_loan = form.outstanding_loan.data
        member.disability = form.disability.data
        member.apl = form.apl.data
        member.soc_category = form.soc_category.data
        member.religion = form.religion.data
        member.age = form.age.data
        db.session.commit()
        flash('Member has been updated!', 'success')
        return redirect(url_for('member', shg_id=shg.id, member_id=member_id))
    elif request.method == 'GET':
        form.name.data = member.name
        form.spouse_father.data = member.spouse_father
        form.gender.data = member.gender
        form.outstanding_loan.data = member.outstanding_loan
        form.disability.data = member.disability
        form.apl.data = member.apl
        form.soc_category.data = member.soc_category
        form.religion.data = member.religion
        form.age.data = member.age
    return render_template('add_update_member.html', title='Update Member',
                           form=form, legend='Update Member')


@app.route("/shg/<int:shg_id>/member/<int:member_id>/delete", methods=['POST'])
@login_required
def delete_member(shg_id, member_id):
    """
    Deletes the details of SHG member with ID member_id from database
    :param shg_id: Input SHG ID stored in db of the shg whose member is to be deleted
    :param member_id: Input Member ID stored in db of the shg member whose details are to be deleted.
    :return: Redirects to the home page after deleting the member.
    """
    # shg = Shg.query.get_or_404(shg_id)
    member = Member.query.get_or_404(member_id)
    if member.shg.coordinator.id != current_user.id:
        os.abort(403)
    member.shg.num_members -= 1
    db.session.delete(member)
    db.session.commit()
    flash('Member has been deleted!', 'success')
    return redirect(url_for('shg', shg_id=shg_id))


@app.route("/shg/<int:shg_id>/evaluation", methods=['GET', 'POST'])
def eval_shg(shg_id):
    """
    Details of shg are taken and evaluated according to the standard practice followed in Haryana urban local bodies
    department.
    :param shg_id: Input SHG ID stored in db of the shg whose details are to be evaluated.
    """
    shg = Shg.query.get_or_404(shg_id)
    members = Member.query.filter_by(shg_id=shg.id)
    soc_category_dict = {'general': 0.9, 'obc': 1.25, 'sc': 1.5, 'st': 1.5, 'other': 1.5}
    gender_dict = {'male': 0.9, 'female': 1.25, 'other': 2}
    soc_category_breakdown = {'general': 0, 'obc': 0, 'sc': 0, 'st': 0, 'other': 0}
    num_members = len(list(members))
    gender_score = 0
    disabled_count = 0
    minority_count = 0
    bc_score = 0
    # obc, sc, st = 0, 0, 0
    bpl_count = 0
    outstanding_loans = []
    for member in members:
        bc_score += soc_category_dict[member.soc_category]
        gender_score += gender_dict[member.gender]
        outstanding_loans.append(int(member.outstanding_loan))
        soc_category_breakdown[member.soc_category] += 1
        if member.religion in ['muslim', 'buddhist', 'other']:
            minority_count += 1
        if member.apl != 'apl':
            bpl_count += 1
        if member.disability == 'yes':
            disabled_count += 1
    soc_score = (5 * bc_score / (1.5 * num_members)) + (2 * gender_score / (2 * num_members)) + (
            disabled_count / num_members) + \
                (minority_count / num_members) + (bpl_count / num_members)
    loan_conc_index = sum((loan / (0.5 * shg.total_savings * num_members)) ** 2 for loan in outstanding_loans)
    if loan_conc_index <= 0.15:
        default_risk = 'low'
    elif 0.15 < loan_conc_index <= 0.25:
        default_risk = 'medium'
    else:
        default_risk = 'high'

    return render_template('eval_shg.html', title=shg.name, shg=shg, members=members, num_members=num_members,
                           gender_score=gender_score, disabled_count=disabled_count, minority_count=minority_count,
                           soc_category_breakdown=soc_category_breakdown,
                           bc_score=bc_score, bpl_count=bpl_count, loan_conc_index=loan_conc_index,
                           default_risk=default_risk, soc_score=soc_score / 10)


@app.route("/shg/<int:shg_id>/member/<int:member_id>/evaluation", methods=['GET', 'POST'])
def eval_member(shg_id, member_id):
    """
    Details of member are taken and evaluated according to the standard practice followed in Haryana urban local bodies
    department.
    :param shg_id: Enter the SHG ID stored in db of the shg whose details are to be evaluated.
    :param member_id: Enter the Member ID stored in db of the member whose details are to be evaluated.
    """

    member = Member.query.get_or_404(member_id)
    member_meetings = member_meeting.query.filter_by(member_id=member.id)
    num_meetings = len(list(member_meetings))
    schemes_list = {'general': ['Mahatma Gandhi National Rural Employment Guarantee Act', 'Awas Yojana',
                                'Swacch Bharath Abhiyaan', 'Krishi Vikas Yojana',
                                'Rashtriya Swasthya Bima Yojana', 'Deen Dayal Upadhyaya Grameen Kaushalya Yojana',
                                'Pradhan Mantri Matritva Vandana Yojana', 'Integrated Child Development Services',
                                'Pradhan Mantri Kaushal Vikas Yojna', 'NRLM'],
                    'obc': ['All schemes in General Category', 'Free Coaching for SC and OBC students',
                            'Dr. Ambedkar Pre-Matric and Post-Matric Scholarship',
                            'Dr. Ambedkar Post-Matric Scholarship for EBCs',
                            'National Fellowship for OBC Students (NF-OBC)'
                            ],
                    'sc': ['All schemes in General Category', 'Pre-matriculate scholarships for SC students',
                           'Post-matriculate scholarships for SC students',
                           'National Fellowship', 'National Overseas Scholarship',
                           'Free Coaching for SC and OBC students',
                           'Venture Capital Fund for Scheduled Castes',
                           'Credit Enhancement Guarantee Scheme for Scheduled Castes',
                           'Babu Jagjivan Ram Chatrawas Yojana'],
                    'st': ['All schemes in General Category', 'Pre-matriculate scholarships for SC students',
                           'Post-matriculate scholarships for SC students',
                           'Rajiv Gandhi National Fellowship', 'National Overseas Scholarship', 'Central Hostel Scheme',
                           'Eklavya Residential School Scheme', 'Vocational Training Schemes for Scheduled Tribes'],
                    'other': 1.5}
    schemes = schemes_list[member.soc_category]
    if member.soc_category != 'general':
        schemes += schemes_list['general']

    present = 0
    loans_taken = []
    loans_repaid = []
    bank_visits = 0
    govt_visits = 0

    for meeting in member_meetings:
        if meeting.attended == 'yes':
            present += 1
        loans_taken.append(meeting.loan_taken)
        loans_repaid.append(meeting.loan_repaid)
        if meeting.bank_visits == 'yes':
            bank_visits += meeting.bank_visits
        if meeting.govt_visits == 'yes':
            govt_visits += meeting.govt_visits
    return render_template('eval_member.html', title=member.name, present=present, loans_taken=sum(loans_taken),
                           loans_repaid=sum(loans_repaid), bank_visits=bank_visits, govt_visits=govt_visits,
                           shg_id=shg_id, member_meetings=member_meetings, member=member, num_meetings=num_meetings,
                           schemes=schemes)


# This is unused now since adding separate member meeting details.
@app.route("/shg/<int:shg_id>/meeting/add", methods=['GET', 'POST'])
@login_required
def add_shg_meeting(shg_id):
    shg = Shg.query.get_or_404(shg_id)
    form = SHGMeetingForm()
    shg_members = list(shg.members)
    subforms = [MemberMeetingForm() for _ in shg_members]
    if form.validate_on_submit():
        meeting = shg_meeting(date=form.date.data, attendance=0, shg_id=shg_id)
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting Details have been successfully added!', 'success')
        return redirect(url_for('shg', shg_id=shg.id))
    return render_template('add_shg_meeting.html', title='New SHG Meeting', form=form, subforms=subforms,
                           shg_members=shg_members, legend='New SHG Meeting')


@app.route("/shg/<int:shg_id>/<int:member_id>/meeting/add", methods=['GET', 'POST'])
@login_required
def add_member_meeting(shg_id, member_id):
    """
    SHGs have regular meetings. Here the details for each member for a meeting are updated.
    :param shg_id: SHG ID of the shg to which the member whose meeting details are to be added.
    :param member_id: Member ID of the member whose meeting details are to be added.
    :return: Redirects to the SHG page
    """
    shg = Shg.query.get_or_404(shg_id)
    member = Member.query.get_or_404(member_id)
    form = MemberMeetingForm()
    if form.validate_on_submit():
        member_meet = member_meeting(date=form.date.data, attended=form.attended.data, amt_paid=form.amt_paid.data,
                                     bank_visits=form.bank_visits.data, govt_visits=form.govt_visits.data,
                                     debt=form.debt.data, loan_taken=form.loan_taken.data,
                                     loan_repaid=form.loan_repaid.data, member_id=member_id)
        db.session.add(member_meet)
        db.session.commit()
        flash('Member Meeting Details have been successfully added!', 'success')
        return redirect(url_for('member', shg_id=shg.id, member_id=member.id))
    return render_template('add_member_meeting.html', title="New SHG Meeting", form=form,
                           legend="Update details of Member"
                                  " at SHG Meeting")


@app.route("/shg/<int:shg_id>/<int:member_id>/meeting/view", methods=['GET', 'POST'])
@login_required
def view_member_meetings(shg_id, member_id):
    """
    SHGs have regular meetings. Here the details for each member for past meetings are displayed.
    :param shg_id: SHG ID of the shg to which the member whose meeting details are to be displayed.
    :param member_id: Member ID of the member whose meeting details are to be displayed.
    :return: Redirects to the SHG page
    """
    shg = Shg.query.get_or_404(shg_id)
    member = Member.query.get_or_404(member_id)
    member_meetings = member_meeting.query.filter_by(member_id=member.id)
    return render_template('member_meeting_history.html', title=member.name, shg=shg, member=member,
                           member_meetings=member_meetings)
