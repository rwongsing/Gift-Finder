from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, URL
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/robert/Coding/Website Terminal/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    
    web1 = db.Column(db.String(80))
    link1 = db.Column(db.String(80))
    web2 = db.Column(db.String(80))
    link2 = db.Column(db.String(80))
    web3 = db.Column(db.String(80))
    link3 = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class addForm(FlaskForm):
    website = StringField('website', validators=[InputRequired(), Length(min=1, max=20)])
    link = StringField('link', validators=[InputRequired(), URL(message='Invalid link')])

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        
        message = 'Invalid username or password'     
        return render_template('message.html', message=message)
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,)
        db.session.add(new_user)
        db.session.commit()

        message = 'New user has been created'     
        return render_template('message.html', message=message)
    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username, web1=current_user.web1, link1=current_user.link1,
    web2=current_user.web2, link2=current_user.link2, web3=current_user.web3, link3=current_user.link3)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    message = 'User has been successfully signed out'
    return render_template('message.html', message=message)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = addForm()

    if form.validate_on_submit():
        if current_user.web1 == None:
            current_user.web1 = form.website.data
            current_user.link1 = form.link.data
        elif current_user.web2 == None:
            current_user.web2 = form.website.data
            current_user.link2 = form.link.data
        elif current_user.web3 == None:
            current_user.web3 = form.website.data
            current_user.link3 = form.link.data
        else:
            message='Error: All slots are filled. Please delete a slot.'
            return render_template('message.html', message=message)
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)