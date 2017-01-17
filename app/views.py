from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/') #Route 'decorators' -- Creates the mapping for the URLS /
@app.route('/index') #This route decorator creates a mapping for the /index URL

def index():
  user = {'nickname': 'Anthony'} #fake!
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
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for OpenID="%s", remember_me=%s' %
          (form.openid.data, str(form.remember_me.data)))
    return redirect('/index')
  return render_template('login.html',
                          title='Sign In',
                          form=form,
                          providers=app.config['OPENID_PROVIDERS'])
