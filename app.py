from flask import Flask, render_template, flash, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm, FeedBackForm, ForgotPassword, PersonalInfoForm, ExperienceForm, AcademicForm, SkillForm, ResetPasswordForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = b'\x7f \x92\xa10\x80\x13\xac\xf7R\xcc\x18\x8e\x05Ojk>x9\x94\xb0\xeem'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///resumedb.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '' # Your e-mail
app.config['MAIL_PASSWORD'] = '' # Your password
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
CSRF_ENABLED = True
db = SQLAlchemy(app)
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class AddressData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(20),unique=True,nullable=False)
    door1 = db.Column(db.String(10),nullable=False)
    door2 = db.Column(db.String(10),nullable=False)
    district1 = db.Column(db.String(20),nullable=False)
    district2 = db.Column(db.String(20),nullable=False)
    city1 = db.Column(db.String(25),nullable=False)
    city2 = db.Column(db.String(265),nullable=False)
    state1 = db.Column(db.String(30),nullable=False)
    state2 = db.Column(db.String(30),nullable=False)
    pincode1 = db.Column(db.String(6),nullable=False)
    pincode2 = db.Column(db.String(6),nullable=False)

class SSCData(db.Model):
    user = db.Column(db.String(20),primary_key=True)
    ssc_inst = db.Column(db.String(30),nullable=False)
    ssc_join = db.Column(db.Integer,nullable=False)
    ssc_passout = db.Column(db.Integer,nullable=False)
    ssc_inst_city = db.Column(db.String(30),nullable=False)
    ssc_score = db.Column(db.String(4),nullable=False)

class HigherSecData(db.Model):
    user = db.Column(db.String(20),primary_key=True)
    dip_inter = db.Column(db.String(13),nullable=False)
    di_inst = db.Column(db.String(30),nullable=False)
    di_join = db.Column(db.Integer,nullable=False)
    di_passout = db.Column(db.Integer,nullable=False)
    di_inst_city = db.Column(db.String(30),nullable=False)
    di_score = db.Column(db.String(4),nullable=False)

class UGData(db.Model):
    user = db.Column(db.String(20),primary_key=True)
    ug_inst = db.Column(db.String(30),nullable=False)
    ug_degree = db.Column(db.String(20),nullable=False)
    ug_branch = db.Column(db.String(30),nullable=False)
    ug_join = db.Column(db.Integer,nullable=False)
    ug_passout = db.Column(db.Integer,nullable=False)
    ug_inst_city = db.Column(db.String(30),nullable=False)
    ug_score = db.Column(db.String(4),nullable=False)

class PGData(db.Model):
    user = db.Column(db.String(20),primary_key=True)
    pg_inst = db.Column(db.String(30),nullable=False)
    pg_degree = db.Column(db.String(20),nullable=False)
    pg_branch = db.Column(db.String(30),nullable=False)
    pg_join = db.Column(db.Integer,nullable=False)
    pg_passout = db.Column(db.Integer,nullable=False)
    pg_inst_city = db.Column(db.String(30),nullable=False)
    pg_score = db.Column(db.String(4),nullable=False)

class PersonalData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(20),unique=True,nullable=False)
    firstname = db.Column(db.String(30),nullable=False)
    lastname = db.Column(db.String(20),nullable=False)
    middlename = db.Column(db.String(20),nullable=True)
    dob = db.Column(db.String(10),nullable=False)
    pemail = db.Column(db.String(30),nullable=False)
    semail = db.Column(db.String(30),nullable=False)
    pcontact = db.Column(db.String(12),nullable=False)
    scontact = db.Column(db.String(12),nullable=True)
    des = db.Column(db.Text,nullable=False)

class ExperienceData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(20),nullable = False)
    company = db.Column(db.String(30),nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    position = db.Column(db.String(30),nullable = False)

class ProjectsData(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(20),nullable=False)
    title = db.Column(db.String(30),nullable=False)
    des = db.Column(db.String(1000),nullable=False)

class URLData(db.Model):
    user = db.Column(db.String(20),primary_key=True)
    facebook = db.Column(db.String(100),nullable=True,unique=True)
    twitter = db.Column(db.String(100),nullable=True,unique=True)
    linkedin = db.Column(db.String(100),nullable=True,unique=True)
    stack_overflow = db.Column(db.String(100),nullable=True,unique=True)
    github = db.Column(db.String(100),nullable=True,unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(40),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    image = db.Column(db.String(50),nullable=False,default='default.jpg')

    def get_reset_token(self,expire_sec=6000):
        s = Serializer(app.config['SECRET_KEY'],expire_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self,user,email,password):
        self.user = user
        self.email = email
        self.password = password

class feedback(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(40),nullable=False)
    feed_type = db.Column(db.String(15),nullable=False)
    message = db.Column(db.Text,nullable=False)

    def __init__(self,name,email,feed_type,message):
        self.name = name
        self.email = email
        self.feed_type = feed_type
        self.message = message

class Skills(db.Model):
    user = db.Column(db.String(30),nullable=False,primary_key=True)
    soft_skills = db.Column(db.String(200),nullable=False)
    tech_skills = db.Column(db.String(200),nullable=False)
    langs_known = db.Column(db.String(100),nullable=False)
    #skillevel = db.Column(db.String(10),nullable=False)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@orm.com',recipients=[user.email])
    msg.body = f'''To reset your Password, Visit the Following Link.
    {url_for('resetPassword',token=token,_external=True)}

    If You did not not made this request, then simply ignore it.
    '''
    mail.send(msg)

@app.route('/')
def index():
    return render_template('index.html',title="ORM - Online Resume Management")
  
@app.route('/Login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(user=form.user.data).first()
        if user and user.password == form.password.data:
            login_user(user,remember = form.remember.data)
            if PersonalData.query.filter_by(user=current_user.user).first():
                return redirect(url_for('dashboard'))
            return redirect(url_for('personal'))
        else:
            flash("Incorrect Username or Password",'info')
    return render_template('login.html',title="ORM - Login",form=form)

@app.route('/SignUp',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        if User.query.filter_by(user=form.user.data).first() or User.query.filter_by(email=form.email.data).first():
            flash('Username or Email already exists!','danger')
            return redirect(url_for('signup'))
        else:
            u = User(user=form.user.data,email=form.email.data,password=form.password.data)
            db.session.add(u)
            db.session.commit()
            flash('Your account has been created sucessfully! You can login now!','success')
            return redirect(url_for('login'))
    return render_template('signup.html',title="ORM - Sign Up",form=form)

@app.route('/Feedback', methods = ['GET', 'POST'])
@login_required
def feed_back():
    form = FeedBackForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        feed_type = form.select.data
        message = form.message.data
        f = feedback(name,email,feed_type,message)
        db.session.add(f) 
        db.session.commit()
        flash('Thank You! Your response has been saved! We will get back to you soon.','success')
        return render_template('feedback.html',title="ORM - Feedback",form=form)
    return render_template('feedback.html',title="ORM - Feedback",form=form)

@app.route('/About_Us')
def about_us():
    return render_template('about_us.html',title="ORM - About Us")

@app.route('/ForgotPassword',methods=["GET","POST"])
def forgotPassword():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgotPassword()
    if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       send_reset_email(user) 
    return render_template('forgotpassword.html',form=form,title='ORM - Forgot Password')

@app.route('/ForgotPassword/<token>',methods=["GET","POST"])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired password reset link','warning')
        return redirect(url_for('forgotPassword'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.new_password.data
        db.session.commit()
        flash('Your Password has been Updated! You can login now.','info')
        return redirect(url_for('login'))
    return render_template('resetpassword.html',form=form,title="ORM - Reset Password")

@app.route('/Academic',methods=["GET","POST"])
@login_required
def academic():
    form = AcademicForm()
    if request.method == "POST":
        ssc = SSCData(user=current_user.user,ssc_inst=form.ssc.instituteName.data,ssc_join=form.ssc.joiningYear.data,ssc_passout=form.ssc.passOutYear.data,ssc_inst_city=form.ssc.instituteAddress.data,ssc_score=form.ssc.score.data)
        dip = HigherSecData(user=current_user.user,dip_inter=form.diporint.data,di_inst=form.dip_int.instituteName.data,di_join=form.dip_int.joiningYear.data,di_passout=form.dip_int.passOutYear.data,di_inst_city=form.dip_int.instituteAddress.data,di_score=form.dip_int.score.data)
        ug = UGData(user=current_user.user,ug_inst=form.ug.instituteName.data,ug_degree=form.ug_stream.data,ug_branch=form.ug_branch.data,ug_join=form.ug.joiningYear.data,ug_passout=form.ug.passOutYear.data,ug_inst_city=form.ug.instituteAddress.data,ug_score=form.ug.score.data)
        db.session.add_all([ssc,dip,ug])
        db.session.commit()
        return render_template('display.html',user=form.ssc.instituteName.data)
    return render_template('academic.html',form=form,title='ORM - Academic Details')

@app.route('/OtherSkills',methods=["GET","POST"])
@login_required
def skills():
    form = SkillForm()
    if request.method == "POST":
        soft = json.dumps(form.soft_skills.data)
        tech = json.dumps(form.tech_skills.data)
        langs = json.dumps(form.langs_known.data)
        urls = URLData(user=current_user.user,facebook=form.urls.facebook.data,twitter=form.urls.twitter.data,linkedin=form.urls.linkedin.data,stack_overflow=form.urls.stack_overflow.data,github=form.urls.github.data)
        sk = Skills(user=current_user.user,soft_skills=soft,tech_skills=tech,langs_known=langs)
        db.session.add_all([urls,sk])
        db.session.commit()
        return render_template('display.html',user=json.dumps(soft))
    return render_template('skills.html',form=form,title='ORM - Skills')

@app.route('/Personal',methods=["GET","POST"])
@login_required
def personal():
    form = PersonalInfoForm()
    if request.method == "POST":
        pdata = PersonalData(user=current_user.user,firstname = form.firstName.data,lastname=form.lastName.data,middlename=form.middleName.data,dob=str(form.dob.data.day)+'-'+str(form.dob.data.month)+'-'+str(form.dob.data.year),pemail = form.emailPrimary.data,semail=form.emailSecondary.data,pcontact=form.contactPrimary.data,scontact=form.contactSecondary.data,des = form.description.data)
        # db.session.add(pdata)
        address = AddressData(user=current_user.user,door1=form.permanentAddress.door_number.data,
        door2=form.currentAddress.door_number.data,district1=form.permanentAddress.district.data,
        district2=form.currentAddress.district.data,city1=form.permanentAddress.city.data,
        city2=form.currentAddress.city.data,state1=form.permanentAddress.state.data,
        state2=form.currentAddress.state.data,pincode1=form.permanentAddress.pincode.data,
        pincode2=form.currentAddress.pincode.data)
        db.session.add_all([pdata,address])
        db.session.commit()
        return redirect(url_for('academic'))
    return render_template('personal.html',form=form,title="ORM - Personal Details")


@app.route('/Dashboard')
@login_required
def dashboard():
    data = {
        'personal':PersonalData.query.filter_by(user=current_user.user).first(),
        'address':AddressData.query.filter_by(user=current_user.user).first(),
        'edu':{
            'ssc':SSCData.query.filter_by(user=current_user.user).first(),
            'di':HigherSecData.query.filter_by(user=current_user.user).first(),
            'ug':UGData.query.filter_by(user=current_user.user).first(),
            'pg':PGData.query.filter_by(user=current_user.user).first()
        },
        'exp':ExperienceData.query.filter_by(user=current_user.user).all(),
        'urls':URLData.query.filter_by(user=current_user.user).first(),
        'skills': Skills.query.filter_by(user=current_user.user).all(),
        'proj' : ProjectsData.query.filter_by(user=current_user.user).all()
    }
    return render_template('dashboard.html',data=data,title=current_user.user + ' - ORM',tech = ['Java','C','C++','Content Writing','SEO'])

@app.route('/AddSkill')
def addskill():
    form=SkillForm()
    return render_template('addskill.html',form=form)

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html',title="ORM - FAQ's")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    db.create_all()
    app.run()
