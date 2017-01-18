from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User


@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.before_request
def before_request():
  g.user = current_user

@app.route('/') #Route 'decorators' -- Creates the mapping for the URLS /
@app.route('/index') #This route decorator creates a mapping for the /index URL
@login_required
def index():
  user = g.user
  posts = [ #array of posts that are fake
      {
        'author': {'nickname': 'Anthony'},
        'body': 'Test post for microblog Python tutorial',
        'category': 'Updates'
      },
      {
        'author': {'nickname': 'Anthony'},
          'body': 'Test post for microblog Python tutorial.  The quick brown fox jumps over the lazy dog.  It was the best of times, it was the worst of times',
           'category': 'News'
      }


  ]
  return render_template("index.html",
                          title='Home',
                          user=user,
                          posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticaed:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
  return render_template('login.html',
                          title='Sign In',
                          form=form,
                          providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp): #gets information returned from the OID provider
  if resp.email is None or resp.email == "":  #determines if the email exists or not
    flash('Invalid login.  Please try again.') #if not found, report error
    return redirect(url_for('login')) #returns back to login page
  user = User.query.filter_by(email=resp.email).first() #searches the db for email
  if user is None: #if it isn't found...
    nickname = respo.nickname
    if nickname is None or nickname == "":
      nickname = resp.email.split('@')[0]
    user = User(nickname=nickname, email=resp.email)
    db.session.add(user) #...create a new user
    db.session.commit() # and commit the database
  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me', None)
  login_user(user, remember = remember_me) #after everything is happy, login
  return redirect(request.args.get('next') or url_for('index')) #redirect to index/homepage
