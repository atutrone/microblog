from flask import render_template
from app import app

@app.route('/') #Route 'decorators' -- Creates the mapping for the URLS /
@app.route('/index') #This route decorator creates a mapping for the /index URL

def index():
  user = {'nickname': 'Anthony'} #fake!
  posts = [ #array of posts that are fake
      {
        'author': {'nickname': 'Anthony'},
        'body': 'Test post for microblog Python tutorial'
      },
      {
        'author': {'nickname': 'Anthony'},
        'body': 'Test post for microblog Python tutorial'
      }


  ]
  return render_template("index.html",
                          title='Home',
                          user=user,
                          posts=posts)
