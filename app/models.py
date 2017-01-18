from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  '''indicates a 'one-to-many' relationship which is why it's declared in the User class.  This relationship provides us with a way to call all posts belonging to a particular user from the User class perspective.  "One" is the user and "Many" is the posts that are associated with the 'author' found in the 'backref' argument'''

  @property
  def is_authenticated(self):
    return True

  @property
  def is_active(self):
    return True

  @property
  def is_anonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id) #Python2
    except NameError:
      return st(self.id) #Python3

  def __repr__(self):
    return '<User %r>' % (self.nickname)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post %r>' % (self.body)

'''user_id was initialized as a ForeignKey so that Flask-SQLAlchemy knows that this particular field will be linked to the id variable declared in the User class'''

