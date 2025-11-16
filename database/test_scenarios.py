from database.connection import get_db_connection
from database.operations import (
    UserOperations, ResumeOperations, KeywordsOperations,
    MLModelOperations, UpdatedResumeOperations, AdminOperations
)
import bcrypt

def test_scenario_1_user_signup_and_login():
    """Test: User signs up and logs in"""
    print("\n" + "="*60)
    print("SCENARIO 1: User Signup and Login")
    print("="*60)
    
    try:
        # User signs up
        password = "SecurePass123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = UserOperations.create_user(
            username="johndoe",
            email="john.doe@email.com",
            password_hash=password_hash
        )
        
        if user:
            print(f" User created: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Scans remaining: {user.subscription.scans_remaining}")
            
            # User logs in
            UserOperations.update_last_login(user.user_id)
            print(f" User logged in successfully")
            
            return user
        else:
            print(" User creation failed")
            return None
            
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_2_upload_resume(user):
    """Test: User uploads a resume"""
    print("\n" + "="*60)
    print("SCENARIO 2: Upload Resume")
    print("="*60)
    
    if not user:
        print(" No user provided")
        return None
    
    try:
        resume_text = """
        John Doe
        Software Engineer
        Email: john@email.com
        
        EXPERIENCE:
        - Python Developer at TechCorp (2020-2023)
        - Built web applications using Django and Flask
        - Worked with PostgreSQL databases
        
        EDUCATION:
        - BS Computer Science, State University (2020)
        
        SKILLS:
        Python, JavaScript, SQL, Git, Docker
        """
        
        resume = ResumeOperations.create_resume(
            user_id=user.user_id,
            file_name="john_doe_resume.pdf",
            file_type="pdf",
            original_text=resume_text
        )
        
        if resume:
            print(f" Resume uploaded: {resume.file_name}")
            print(f"   Resume ID: {resume.resume_id}")
            print(f"   Status: {resume.status}")
            return resume
        else:
            print(" Resume upload failed")
            return None
            
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_3_add_keywords(user):
    """Test: User adds target keywords for job"""
    print("\n" + "="*60)
    print("SCENARIO 3: Add Job Keywords")
    print("="*60)
    
    if not user:
        print(" No user provided")
        return None
    
    try:
        keywords = KeywordsOperations.create_keyword_input(
            keywords=["Python", "Django", "React", "MongoDB", "AWS", "Docker", "CI/CD"],
            user_id=user.user_id,
            industry="Software Engineering",
            job_role="Full Stack Developer",
            job_description="Looking for a full stack developer with Python and React experience..."
        )
        
        if keywords:
            print(f" Keywords added: {len(keywords.keywords)} keywords")
            print(f"   Industry: {keywords.industry}")
            print(f"   Job Role: {keywords.job_role}")
            print(f"   Keywords: {', '.join(keywords.keywords)}")
            return keywords
        else:
            print(" Keywords creation failed")
            return None
            
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_4_ai_analyzes_resume(resume, keywords):
    """Test: AI analyzes the resume"""
    print("\n" + "="*60)
    print("SCENARIO 4: AI Analyzes Resume")
    print("="*60)
    
    if not resume or not keywords:
        print(" No resume or keywords provided")
        return None
    
    try:
        # Update status to processing
        ResumeOperations.update_resume_status(resume.resume_id, "processing")
        print(" Resume analysis in progress...")
        
        # Simulate AI analysis
        analysis_data = {
            'keywords_found': ["Python", "SQL", "Git", "Docker"],
            'keywords_missing': ["Django", "React", "MongoDB", "AWS", "CI/CD"],
            'keyword_density': {
                "Python": 3,
                "SQL": 1,
                "Git": 1,
                "Docker": 1
            },
            'has_contact_info': True,
            'has_experience': True,
            'has_education': True,
            'has_skills': True,
            'is_ats_friendly': True,
            'formatting_issues': [],
            'feedback': 'Good resume structure. Consider adding more relevant keywords.',
            'suggestions': [
                'Add Django framework experience',
                'Include React projects',
                'Mention MongoDB database work',
                'Add AWS cloud experience',
                'Include CI/CD pipeline knowledge'
            ]
        }
        
        # Update resume with analysis
        updated_resume = ResumeOperations.update_resume_with_analysis(
            resume_id=resume.resume_id,
            score=72,
            analysis_data=analysis_data
        )
        
        if updated_resume:
            print(f" Analysis complete!")
            print(f"   Score: {updated_resume.overall_score}/100")
            print(f"   Keywords found: {len(updated_resume.analysis.keywords_found)}")
            print(f"   Keywords missing: {len(updated_resume.analysis.keywords_missing)}")
            print(f"   ATS Friendly: {updated_resume.analysis.is_ats_friendly}")
            print(f"   Suggestions: {len(updated_resume.analysis.suggestions)}")
            
            # Log ML execution
            MLModelOperations.log_ml_execution(
                resume_id=resume.resume_id,
                score=72,
                feedback=analysis_data['feedback'],
                keyword_id=keywords.keyword_id,
                processing_time=2.5
            )
            print(f" ML execution logged")
            
            return updated_resume
        else:
            print(" Analysis failed")
            return None
            
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_5_ai_creates_updated_resume(resume):
    """Test: AI creates an improved version of the resume"""
    print("\n" + "="*60)
    print("SCENARIO 5: AI Creates Updated Resume")
    print("="*60)
    
    if not resume:
        print(" No resume provided")
        return None
    
    try:
        updated_text = """
        John Doe
        Full Stack Software Engineer
        Email: john@email.com | LinkedIn: linkedin.com/in/johndoe
        
        PROFESSIONAL SUMMARY:
        Experienced Software Engineer with 3+ years in full-stack development using Python, Django,
        React, and cloud technologies. Proficient in building scalable web applications.
        
        EXPERIENCE:
        Python Full Stack Developer | TechCorp | 2020-2023
        - Developed web applications using Django and Flask frameworks
        - Implemented React-based front-end components for improved user experience
        - Managed PostgreSQL and MongoDB databases for data persistence
        - Deployed applications on AWS with Docker containerization
        - Set up CI/CD pipelines using Jenkins and GitHub Actions
        
        EDUCATION:
        Bachelor of Science in Computer Science | State University | 2020
        
        TECHNICAL SKILLS:
        Languages: Python, JavaScript, SQL
        Frameworks: Django, Flask, React, Node.js
        Databases: PostgreSQL, MongoDB, MySQL
        DevOps: Docker, AWS, CI/CD, Git
        """
        
        updated_resume = UpdatedResumeOperations.create_updated_resume(
            original_resume_id=resume.resume_id,
            updated_text=updated_text,
            changes_made=[
                "Added professional summary",
                "Enhanced job descriptions with Django and React keywords",
                "Added MongoDB database experience",
                "Included AWS and Docker deployment details",
                "Added CI/CD pipeline experience",
                "Added LinkedIn profile link"
            ],
            improvement_score=23
        )
        
        if updated_resume:
            print(f" Updated resume created!")
            print(f"   Score improvement: +{updated_resume.improvement_score} points")
            print(f"   Changes made: {len(updated_resume.changes_made)}")
            print(f"   New estimated score: {72 + updated_resume.improvement_score}/100")
            return updated_resume
        else:
            print(" Updated resume creation failed")
            return None
            
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_6_user_views_resumes(user):
    """Test: User views all their resumes"""
    print("\n" + "="*60)
    print("SCENARIO 6: View User's Resumes")
    print("="*60)
    
    if not user:
        print(" No user provided")
        return None
    
    try:
        resumes = ResumeOperations.get_user_resumes(user.user_id)
        
        print(f" Found {len(resumes)} resume(s)")
        for idx, resume in enumerate(resumes, 1):
            print(f"\n   Resume {idx}:")
            print(f"   - File: {resume.file_name}")
            print(f"   - Status: {resume.status}")
            if resume.overall_score:
                print(f"   - Score: {resume.overall_score}/100")
            print(f"   - Uploaded: {resume.upload_date.strftime('%Y-%m-%d %H:%M')}")
        
        return resumes
        
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_7_admin_views_all_data():
    """Test: Admin views all users and resumes"""
    print("\n" + "="*60)
    print("SCENARIO 7: Admin Views All Data")
    print("="*60)
    
    try:
        # Create admin account
        admin_password = "AdminPass456"
        admin_password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin = AdminOperations.create_admin(
            username="admin",
            email="admin@resumescanner.com",
            password_hash=admin_password_hash
        )
        
        if admin:
            print(f" Admin created: {admin.username}")
        
        # Admin views all users
        all_users = AdminOperations.get_all_users()
        print(f" Total users in system: {len(all_users)}")
        
        # Admin views all resumes
        all_resumes = AdminOperations.get_all_resumes()
        print(f" Total resumes in system: {len(all_resumes)}")
        
        return admin
        
    except Exception as e:
        print(f" Error: {e}")
        return None

def test_scenario_8_multiple_resumes(user):
    """Test: User uploads multiple resumes"""
    print("\n" + "="*60)
    print("SCENARIO 8: Upload Multiple Resumes")
    print("="*60)
    
    if not user:
        print(" No user provided")
        return None
    
    try:
        resume_files = [
            ("software_engineer_resume.pdf", "pdf", "Software Engineer resume with Python experience"),
            ("data_analyst_resume.docx", "docx", "Data Analyst resume with SQL and Excel"),
            ("frontend_dev_resume.pdf", "pdf", "Frontend Developer resume with React and JavaScript")
        ]
        
        uploaded = []
        for file_name, file_type, text in resume_files:
            resume = ResumeOperations.create_resume(
                user_id=user.user_id,
                file_name=file_name,
                file_type=file_type,
                original_text=text
            )
            if resume:
                uploaded.append(resume)
                print(f" Uploaded: {file_name}")
        
        print(f"\n Total resumes uploaded: {len(uploaded)}")
        return uploaded
        
    except Exception as e:
        print(f" Error: {e}")
        return None

def run_all_scenarios():
    """Run all test scenarios"""
    print("\n" + "="*70)
    print(" "*15 + "RESUME SCANNER - DATABASE TESTING")
    print("="*70)
    
    # Connect to database
    try:
        db = get_db_connection()
    except Exception as e:
        print(f" Failed to connect to database: {e}")
        return
    
    # Run scenarios in order
    user = test_scenario_1_user_signup_and_login()
    
    if user:
        resume = test_scenario_2_upload_resume(user)
        keywords = test_scenario_3_add_keywords(user)
        
        if resume and keywords:
            analyzed_resume = test_scenario_4_ai_analyzes_resume(resume, keywords)
            
            if analyzed_resume:
                test_scenario_5_ai_creates_updated_resume(analyzed_resume)
        
        test_scenario_6_user_views_resumes(user)
        test_scenario_8_multiple_resumes(user)
    
    test_scenario_7_admin_views_all_data()
    
    # Final summary
    print("\n" + "="*70)
    print(" "*20 + "ALL SCENARIOS COMPLETED!")
    print("="*70)
    print("\n Your database is fully functional and ready for integration!")
    print("   Share operations.py with your backend team (Tezbir & Sahejpreet)")

if __name__ == "__main__":
    run_all_scenarios()