from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Generic attributes for flask-login Login manager will be imported here
from app import login
from datetime import datetime,date


#------------------BASIC COMPANY USER DETAILS-------------------
@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(db.Model,UserMixin):
	__tablename__ ='user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(256), index=True, unique=True, nullable=False)
	user_type=db.Column(db.String(64))
	third_party_login = db.Column(db.Boolean,default=False)
	password_hash=db.Column(db.String(128), index=True)
	#relationship-----------------
	useremp=db.relationship('Employer', backref='user')
	# user=db.relationship('Employer', backref='employer')

	def user_roll(self):
		return self.user_type

	#-----------Password Hashing---------------------------------
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
    #-----------Chcking if hash and password matches--------------

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Employer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True, nullable=False)
	since=db.Column(db.String(64))
	teamSize=db.Column(db.String(64))
	domain=db.Column(db.String(64))
	desc=db.Column(db.String(3024))
	phone=db.Column(db.String(15))
	website=db.Column(db.String(256))
	address=db.Column(db.String(512))
	logo_url=db.Column(db.String,default=None,nullable=True)
	logo_img_name=db.Column(db.String,default=None,nullable=True)
	#----------------------Relationship----------------------
	posts=db.relationship('Job', backref='employer')
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'))



	#-------------------
 








class Job(db.Model):
	# __table__='job'
	id=db.Column(db.Integer,primary_key=True) 
	title=db.Column(db.String(100))	
	jobdesc=db.Column(db.String(10000))	
	exp=db.Column(db.String(128))	
	qualification=db.Column(db.String(128))	
	career_level=db.Column(db.String(128))	
	email=db.Column(db.String(128))	
	location=db.Column(db.String(50))	
	# roles=db.Column(db.String(128),nullable=False)	
	fulltime=db.Column(db.Boolean,default=False)	
	salary=db.Column(db.String(100))	
	date_posted=db.Column(db.DateTime,default=date.today())	
	expiry_date=db.Column(db.DateTime)	
	openings=db.Column(db.Integer)
	category=db.Column(db.String(128))
	country=db.Column(db.String(100))
	city=db.Column(db.String(100))
	active=db.Column(db.Boolean,default=True);
	#--------------RELATIONSHIP------------------------------
	user_id=db.Column(db.Integer,db.ForeignKey('employer.id'))

 


    
	 

#-----------------------------------------------------------------


	 
