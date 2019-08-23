# This module contains routing for the Jobportal appliction
# All http request will be handled and routed to appropriate template views
# All the form data sent to the application is recieved here

from app import app 
from flask import render_template,request,flash,redirect,url_for,session
from app.models import Employer,Job,User
from app import db
from flask_login import current_user, login_user, logout_user
from datetime import datetime



#-------------------------------------------ROUTING STARTS----------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

#---------------------------------------------HOMEPAGE--------------------------------------------------
@app.route('/')
def index():
	if current_user.is_authenticated:
		return render_template('index.html',current_user=current_user)
	else:
		return render_template('index.html')

#*******************************************************************************************************






#------------------------------------------------SIGNUP--------------------------------------------------
# signup for the companies are done at /register page
@app.route('/register')
def register():
	return render_template('signup1.html')
#********************************************************************************************************





#-----------------------------------REGISTER NEW EMPLOYER-------------------------------------------------

@app.route('/companies/users/add',methods=['POST'])
def add_user():
	if request.method=='POST':
		result=request.form #getting the data sent from form
		uname=result['name'] 
		uemail=result['email']
		upassword=result['password']

		user=User(email=uemail,user_type="Employer")
		user.set_password(upassword)

		db.session.add(user)
		db.session.commit()
		employer=Employer(name=uname,user_id=user.id)
		db.session.add(employer)
		db.session.commit()
		

		return redirect(url_for('index'))
	else:
		return "Oops.! Cannot process this request..!"

#*******************************************************************************************************



#-----------------------------------------LOGIN PAGE FOR CANDIDATES------------------------------------------

@app.route('/candidate/login')
def login_candidate():
	return render_template('login_candidates.html')

#*******************************************************************************************************





#---------------------------------LOGIN PAGE FOR COMPANIES----------------------------------------------

@app.route('/companies/login')
def login_companies():
	return render_template('login_companies.html')

#*******************************************************************************************************



#-------------------------------AUTHENTICATION FOR COMPANIES--------------------------------------------

@app.route('/companies/login/authenticate',methods=['POST','GET'])
def authenticate_company():

	if current_user.is_authenticated:
		user=User.query.get(current_user.get_id())
		if not user.user_roll()=="Employer":
			return "You Don't Permission To Access This Page";
		# already logged in users will be redirected to homepage
		else:
			return redirect(url_for('index'))	

	if request.method=='POST':
		result=request.form
		em=result['email']
		ps=result['password']
		user=User.query.filter_by(email=em).first()
		employer=Employer.query.filter_by(user_id=user.id).first() # querying database for the user details
		if user is None or not user.check_password(ps):  
			return "We cant find your account or you entered a wrong password"
		login_user(user) #Logging in user if authentication is successfull
		return redirect(url_for('index')) # Redirecting to Homepage after successfull authentication


#*******************************************************************************************************
# profile page routering

@app.route('/companies/manage/profile')
def cprofile():
	if current_user.is_authenticated:
		user=User.query.get(current_user.get_id())
		if not user.user_roll()=="Employer":
			return "You Don't Permission To Access This Page";
		employer=Employer.query.filter_by(user_id=user.id).first_or_404()
		return render_template('comprofile.html',user=employer,email=user.email)
	else:
		return redirect(url_for('index'))
	 
	

#------------------------------------------COMPANY PROFILE UPDATE----------------------------------------------

@app.route('/companies/edit/profile',methods=['POST',])
def profile():
	if request.method=='POST':
	 
		req=request.form
		data={}
	 
		if current_user.is_authenticated:
			user=User.query.get(current_user.get_id())
			# emp=Employer.query.filter_by(user_id=current_user.get_id()).first()
			if not user.user_roll()=="Employer":
				return "You Don't have Permission To Access This Page"

			if req['type']=='contact':


				#---------CONTACT INFO UPDATE--------------------

				data['phone']=req['phone']
				data['address']=req['address']
				data['website']=req['website']
				data['email']=req['email']
				
				employer=Employer.query.filter_by(user_id=current_user.get_id()).first_or_404()
				employer.website=data['website']
				employer.address=data['address']
				employer.phone=data['phone']
				employer.email=data['email']
				db.session.commit() #updating the content
				return redirect(url_for('cprofile'))

			else: 
				#--------------- BASIC INFO UPDATE-------------
				data['desc']=req['description']
				data['name']=req['name']
				data['since']=req['since']
				data['size']=req['size']
				data['domain']=req['domain']
				print(data['desc']+data['name']+data['since']+data['size']+data['domain'])
			
				employer=Employer.query.filter_by(user_id=current_user.get_id()).first_or_404()
				employer.name=data['name']
				employer.since=data['since']
				employer.teamSize=data['size']
				employer.domain=data['domain']
				employer.desc=data['desc']
				
				db.session.commit() #updating the content
				return redirect(url_for('cprofile'))

	else:
		return redirect(url_for('login_companies'))
	 

#*******************************************************************************************************
#                  JOB POSTING
# --------------------------------------------------------------------------------------------------------
@app.route('/companies/manage/jobs/post')
def postJob():
	user_data=Employer.query.filter_by(user_id=current_user.get_id()).first_or_404()
	return render_template("post_job.html",user=user_data)

#-------------------add job form request handling--------------------
@app.route('/companies/manage/jobs/post/add',methods=['POST','GET'])
def addjob():
	if request.method=='POST':
		data={}
		req=request.form
		if current_user.is_authenticated:
			user=User.query.get(current_user.get_id())
			if not user.user_roll()=="Employer":
				return "You Don't Permission To Access This Page";
			data['title']=req['title']
			data['description']=req['description']
			#data['email']=req['email']
			data['type']=req['type']
			data['category']=req['category']
			data['experience']=req['experience']
			data['salary']=req['salary']
			data['clevel']=req['clevel']
			data['industry']=req['industry']
			data['qualification']=req['qualification']
			data['deadline']=req['deadline']
			data['country']=req['country']
			data['city']=req['city']
			data['address']=req['address']
			data['openings']=req['openings']
		  
			ft=False;
			if data['type']=='true':
				ft=True
			else:
				ft=False
			today = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
			eid=Employer.query.filter_by(user_id=current_user.get_id()).first_or_404()
			newjob=Job(title=data['title'],jobdesc=data['description'],exp=data['experience'],qualification=data['qualification'],career_level=data['clevel'],location=data['address'],fulltime=ft,city=data['city'],salary=data['salary'],user_id=eid.id,category=data['category'],openings=data['openings'],expiry_date=today)
			db.session.add(newjob)
			db.session.commit()
			print("-----new job added-----")
			return redirect(url_for('manageJob'))
			#return redirect(url_for('index'));	
#-----------MANAGE JOBS-------------------------------------------
@app.route('/companies/manage/job')
def manageJob():
	if current_user.is_authenticated:
		user=User.query.get(current_user.get_id())
		if not user.user_roll()=="Employer":
			return "You Don't Permission To Access This Page"
		employer=Employer.query.filter_by(user_id=current_user.get_id()).first()

		jobs=Job.query.filter_by(user_id=current_user.get_id()).all()
		# for j in jobs:
		# 	print(j.title)
		activeno=0
		for j in jobs:
			if j.active==True:
				activeno+=1;
		rev=reversed(jobs)
		jobposted=len(jobs)
		 
		return render_template("jobmanage.html",user=current_user,joblist=rev,posted=jobposted,active=activeno);

#--------VIEW JOB-------
@app.route('/jobs/<jobid>')
def job(jobid):
	job=Job.query.filter_by(id=jobid).first_or_404()
	company=Employer.query.filter_by(id=job.user_id)
	return render_template("job.html",details=job,emp=company)

#-------------DELETE JOB----------------

@app.route('/jobs/manage/delete/<jobid>')
def deleteJob(jobid):
	print(" job id : "+str(jobid))
	if current_user.is_authenticated:
		user=User.query.get(current_user.get_id())
		print("user role : "+ user.user_roll())
		if not user.user_roll()=="Employer":
			return "Access Denied"
	else:
		return redirect(url_for('login_companies'))

	job=Job.query.filter_by(id=jobid).first_or_404()

	print("jobuserid : "+ str(job.user_id)+ "current_user : "+str(current_user.get_id()))
	temp=current_user.get_id()
	if str(job.user_id) == str(temp):
		# db.session.query(Job).filter(Job.id==jobid).delete()
		Job.query.filter_by(id=jobid).delete()
		db.session.commit();
		print("Deleted : job : "+ jobid)
		return redirect(url_for('manageJob'))
	else:
		return " You Dont Have Permission  to do this operation "

@app.route('/jobs/manage/edit/<jobid>')
def editJob(jobid):
	print(" job id : "+str(jobid))

	jobdet=Job.query.filter_by(id=jobid).first_or_404();
	user=User.query.get(current_user.get_id())
	emp=Employer.query.filter_by(user_id=current_user.get_id()).first_or_404()
	if current_user.is_authenticated:
		if not user.user_roll()=="Employer" or not jobdet.user_id==emp.id:
			return "Access Denied"
	else:
		return redirect(url_for('login_companies'))

	return render_template('editJob.html',user=user,job=jobdet)

@app.route('/jobs/manage/edit/update/<jobid>/',methods=['POST','GET'])
def updateJob(jobid):
	if request.method=='POST':
		print(" job id : "+str(jobid))
		user=User.query.get(current_user.get_id())
		emp=Employer.query.filter_by(user_id=current_user.get_id()).first_or_404()
		job=Job.query.filter_by(id=jobid).first_or_404();
		if current_user.is_authenticated:
		   
			if not user.user_roll()=="Employer" or not job.user_id==emp.id:
				return "***Access Denied***"
		else:
			return redirect(url_for('login_companies'))
		req=request.form

		job.title=req['title']
		job.jobdesc=req['description']
		print("-----------------REACHED HERE____________________")
		job.email=req['email']
		job.type=req['type']
		job.category=req['category']
		job.experience=req['experience']
		job.salary=req['salary']
		job.clevel=req['clevel']
		job.industry=req['clevel']
		job.qualification=req['qualification']
		job.deadline=req['deadline']
		job.country=req['country']
		job.city=req['city']
		job.address=req['address']
		job.openings=req['openings']
		print("-----------------REACHED HERE____________________")
		# return redirect(url_for('manageJob'))
		db.session.commit()
		return redirect(url_for('manageJob'))

#---------------------------------------LOGOUT PAGE-----------------------------------------------------

@app.route('/users/logout')
def logout():
	#logout is dependend on logout_user() of the Flask-login module
	logout_user()
	return redirect(url_for('index'))

#*******************************************************************************************************






 

 