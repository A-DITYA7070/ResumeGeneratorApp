from flask import Flask, request,jsonify
from flask_cors import CORS
from config import db,SECRET_KEY
from os import path,getcwd,environ
from dotenv import load_dotenv
from models.user import User
from models.projects import Projects
from models.educations import Educations
from models.skills import Skills
from models.certificates import Certificates
from models.personalDetails import PersonalDetails
from models.experiences import Experiences

load_dotenv(path.join(getcwd(),'.env'))

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_ECHO']=False
    app.secret_key = SECRET_KEY
    
    db.init_app(app)
    print("DB Initialized successfully..")
    
    with app.app_context():
        @app.route("/signup",methods=['POST'])
        def signup():
            data = request.form.to_dict(flat=True)
            new_user = User(
                username=data['username']
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(msg="user added successfully..")
        @app.route("/add_personal_details",methods=['POST'])
        def add_personal_details():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            data = request.get_json()
            new_personal_details = PersonalDetails(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                linkedin_url=data['linkedin_url'],
                user_id = user.id
            )
            db.session.add(new_personal_details)
            db.session.commit()
            return jsonify(msg="added successfully..")
        
        @app.route('/add_projects',methods=['POST'])
        def add_projects():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            data=request.get_json()
            for user_data in data["data"]:
                user_project=Projects(
                    name=user_data['name'],
                    desc=user_data['desc'],
                    start_date=user_data['start_date'],
                    end_date=user_data['end_date'],
                    user_id=user.id
                )
                db.session.add(user_project)
                db.session.commit()
            return jsonify(msg="added")
        
        @app.route('/add_certificates',methods=['POST'])
        def add_certificates():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            data=request.get_json()
            for user_certificates in data['data']:
                user_cer=Certificates(               
                    title=user_certificates['title'],
                    start_date=user_certificates['start_date'],
                    end_date=user_certificates['end_date'],
                    user_id = user.id
                )
                db.session.add(user_cer)
                db.session.commit()
            return jsonify(msg="added certificates.. ")
        
        @app.route('/add_skills',methods=['POST'])
        def add_skills():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            data=request.get_json()
            for user_skills in data['data']:
                user_skill=Skills(               
                    title=user_skills['title'],
                    confidence_score=user_skills['confidence_score'],
                    user_id = user.id
                )
                db.session.add(user_skill)
                db.session.commit()
            return jsonify(msg="added skills.. ")
        
        @app.route('/add_experiences',methods=['POST'])
        def add_experiences():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            data=request.get_json()
            for user_experience in data['data']:
                user_exper=Experiences(          
                    company_name=user_experience['company_name'],
                    role=user_experience['role'],
                    role_desc=user_experience['role_desc'],
                    start_date=user_experience['start_date'],
                    end_date=user_experience['end_date'],
                    user_id = user.id
                )
                db.session.add(user_exper)
                db.session.commit()
            return jsonify(msg="added experiences.. ")
        
        @app.route('/add_educations',methods=['POST'])
        def add_educations():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            data=request.get_json()
            for user_data in data['data']:
                user_edu=Educations( 
                    school_name=user_data['school_name'],
                    degree_name=user_data['degree_name'],
                    start_date=user_data['start_date'],
                    end_date=user_data['end_date'],
                    user_id = user.id 
                )
                db.session.add(user_edu)
                db.session.commit()
            return jsonify(msg="added educations.. ")
        
        @app.route('/get_resume_json',methods=['GET'])
        def get_resume_json():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            
            personal_details=PersonalDetails.query.filter_by(user_id=user.id).first()
            experiences=Experiences.query.filter_by(user_id=user.id)
            projects=Projects.query.filter_by(user_id=user.id)
            educations=Educations.query.filter_by(user_id=user.id)
            certificates=Certificates.query.filter_by(user_id=user.id)
            skills=Skills.query.filter_by(user_id=user.id)
            
            resume_data={
                "name":personal_details.name,
                "email":personal_details.email,
                "phone":personal_details.phone,
                "address":personal_details.address,
                "linkedin_url":personal_details.linkedin_url
            }
            experiences_data=[]
            projects_data=[]
            educations_data=[]
            certificate_data=[]
            skills_data=[]
            
            # Experience..
            for exp in experiences:
                experiences_data.append({
                    "comapny_name":exp.company_name,
                    "role":exp.role,
                    "role_desc":exp.role_desc,
                    "start_date":exp.start_date,
                    "end_date":exp.end_date
                })
            resume_data["experiences"]=experiences_data
            
            for proj in projects:
                projects_data.append({
                    "name":proj.name,
                    "desc":proj.desc,
                    "start_date":proj.start_date,
                    "end_date":proj.end_date
                })
            resume_data["projects"]=projects_data
            
            for edu in educations:
                educations_data.append({
                "school_name":edu.school_name,
                "degree_name":edu.degree_name,
                "start_date":edu.start_date,
                "end_date":edu.end_date
                })
            resume_data["educations"]=educations_data
            
            for cer in certificates:
                certificate_data.append({
                    "title":cer.title,
                    "start_date":cer.start_date,
                    "end_date":cer.end_date
                })
            resume_data['certificates']=certificate_data
            
            for ski in skills:
                skills_data.append({
                    "title":ski.title,
                    "confidence_score":ski.confidence_score
                })
            resume_data['skills']=skills_data
            
            return jsonify(generatedResume=resume_data)
        # db.drop_all()
        db.create_all()
        db.session.commit()
        return app
    
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  
        
        
    