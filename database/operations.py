from database.models import (
    User, Resume, Admin, KeywordsUserInput, 
    MLModel, UpdatedResume, UserFile, AnalysisResult
)
from datetime import datetime
import uuid

from exceptions import (
    UserNotFoundError,
    ResumeNotFoundError,
    ResumeCreationError,
    KeywordCreationError,
    AdminCreationError,
    AnalysisUpdateError,
)

# User Operations

class UserOperations:
    
    @staticmethod
    def create_user(username, email, password_hash):
        try:
            if User.objects(email=email.lower()).first():
                raise AdminCreationError("A user with this email already exists")
                
            user_id = str(uuid.uuid4())
            user = User(
                user_id=user_id,
                username=username,
                email=email.lower(),
                password=password_hash
            )
            user.save()
            
            user_file = UserFile(user_id=user)
            user_file.save()
            
            return user
        except Exception as e:
            raise AdminCreationError("Failed to create user: {e}")
    
    @staticmethod
    def get_user_by_email(email):
        try:
            user = User.objects(email=email.lower()).first()
            if not user:
                raise UserNotFoundError("User not found")
                
            return user
        except Exception as e:
          raise UserNotFoundError(str(e))
    
    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects(user_id=user_id).first()
            if not user:
                raise UserNotFoundError("User not found")
            return user
        except Exception as e:
            raise UserNotFoundError(str(e))
            
    @staticmethod
    def update_last_login(user_id):
        try:
            user = User.objects(user_id=user_id).first()
            if not user:
                raise UserNotFoundError("User not found")
            
                user.last_login = datetime.now()
                user.save()
                
                user_file = UserFile.objects(user_id=user).first()
                if user_file:
                    user_file.login_count += 1
                    user_file.login_history.append(datetime.now())
                    user_file.save()
                
                return user
        except Exception as e:
            raise UserNotFoundError(f"Failed to update login: {e}")

# Resume Operations

class ResumeOperations:
    
    @staticmethod
    def create_resume(user_id, file_name, file_type, original_text, file_url=None):
        try:
            user = User.objects(user_id=user_id).first()
                if not user:
                    raise UserNotFoundError("User not found")
                    
            resume_id = str(uuid.uuid4())
            
            resume = Resume(
                resume_id=resume_id,
                user_id=user,
                file_name=file_name,
                file_type=file_type,
                original_text=original_text,
                file_url=file_url,
                status="pending"
            )
            resume.save()
            return resume
        except Exception as e:
            raise ResumeCreationError(f"Failed to create resume: {e}")
    
    @staticmethod
    def get_resume_by_id(resume_id):
        try:
            resume = Resume.objects(resume_id=resume_id).first()
            if not resume:
                raise ResumeNotFoundError("Resume not found")
            return resume
        except Exception as e:
            raise ResumeNotFoundError(str(e))
    
    @staticmethod
    def get_user_resumes(user_id):
        try:
            user = User.objects(user_id=user_id).first()
            if not user:
                raise UserNotFoundError("User not found")
                
            return Resume.objects(user_id=user).order_by('-upload_date')
        except Exception as e:
            raise ResumeNotFoundError(f"Failed to fetch resumes: {e}")
    
    @staticmethod
    def update_resume_status(resume_id, status):
        try:
            resume = Resume.objects(resume_id=resume_id).first()
            if not resume:
                raise ResumeNotFoundError("Resume not found.")
                
                resume.status = status
                resume.save()
                return resume
        except Exception as e:
            raise ResumeNotFoundError("Resume not found")
    
    @staticmethod
    def update_resume_with_analysis(resume_id, score, analysis_data):
        # Called by AI component to store analysis results
        try:
            resume = Resume.objects(resume_id=resume_id).first()
            if not resume:
                raise ResumeNotFoundError("Resume not found")
                
                resume.overall_score = score
                resume.scan_date = datetime.now()
                resume.status = "completed"
                
                analysis = AnalysisResult(
                    keywords_found=analysis_data.get('keywords_found', []),
                    keywords_missing=analysis_data.get('keywords_missing', []),
                    keyword_density=analysis_data.get('keyword_density', {}),
                    has_contact_info=analysis_data.get('has_contact_info', False),
                    has_experience=analysis_data.get('has_experience', False),
                    has_education=analysis_data.get('has_education', False),
                    has_skills=analysis_data.get('has_skills', False),
                    is_ats_friendly=analysis_data.get('is_ats_friendly', False),
                    formatting_issues=analysis_data.get('formatting_issues', []),
                    feedback=analysis_data.get('feedback', ''),
                    suggestions=analysis_data.get('suggestions', [])
                )
                
                resume.analysis = analysis
                resume.save()
                return resume
        except Exception as e:
            raise AnalysisUpdateError(f"Failed to update analysis: {e}")
    
    @staticmethod
    def delete_resume(resume_id):
        try:
            resume = Resume.objects(resume_id=resume_id).first()
            if not resume:
                raise ResumeNotFoundError("Resume not found")
          
                resume.delete()
                return True
        except Exception as e:
            raise ResumeNotFoundError(f"Failed to delete resume: {e}")

# Keywords Operations

class KeywordsOperations:
    
    @staticmethod
    def create_keyword_input(keywords, user_id, industry=None, job_role=None, job_description=None):
        try:
            user = User.objects(user_id=user_id).first()
            if not user:
                raise UserNotFoundError("User not found")
            
            keyword_id = str(uuid.uuid4())
            keyword_input = KeywordsUserInput(
                keyword_id=keyword_id,
                keywords=keywords,
                industry=industry,
                job_role=job_role,
                job_description=job_description,
                created_by=user
            )
            keyword_input.save()
            return keyword_input
        except Exception as e:
            raise KeywordCreationError(f"Failed to create keyword input: {e}")
    
    @staticmethod
    def get_keywords_by_id(keyword_id):
        try:
             KeywordsUserInput.objects(keyword_id=keyword_id).first()
            if not keywords:
                raise KeywordCreationError("Keyword input not found")
                return keywords
        except Exception as e:
            raise KeywordCreationError(str(e))

# ML Model Operations

class MLModelOperations:
    
    @staticmethod
    def log_ml_execution(resume_id, score, feedback, keyword_id=None, processing_time=0):
        try:
            resume = Resume.objects(resume_id=resume_id).first()
            if not resume:
                raise ResumeNotFoundError("Resume not found for ML logging")

            keywords = None
            if keyword_id:
            keywords = KeywordsUserInput.objects(keyword_id=keyword_id).first()
            
            ml_result = MLModel(
                resume_id=resume,
                keyword_id=keywords,
                score=score,
                feedback=feedback,
                processing_time=processing_time,
                score_id=str(uuid.uuid4())
            )
            ml_result.save()
            return ml_result
        except Exception as e:
            raise AnalyisUpdateError(f"Failed to log ML execution: {e}")

# Updated Resume Operations

class UpdatedResumeOperations:
    
    @staticmethod
    def create_updated_resume(original_resume_id, updated_text, changes_made, improvement_score):
        try:
            original = Resume.objects(resume_id=original_resume_id).first()
            if not original:
                raise ResumeNotFoundError("Original resume not found")
            
            updated = UpdatedResume(
                resume_id=resume_id,
                original_resume_id=original,
                updated_text=updated_text,
                changes_made=changes_made,
                improvement_score=improvement_score,
                created_by="AI"
            )
            updated.save()
            return updated
        except Exception as e:
            raise AnalysisUpdateError(f"Failed to create updated resume: {e}")
    
    @staticmethod
    def get_updated_resume(original_resume_id):
        try:
            original = Resume.objects(resume_id=original_resume_id).first()
            if not original:
                raise ResumeNotFoundError("Original resume not found")
                
            updated = UpdatedResume.objects(original_resume_id=original).first()
            if not updated:
                raise ResumeNotFoundError("Updated resume not found")
        return updated
        except Exception as e:
            raise ResumeNotFoundError("Updated resume not found")

# Admin Operations

class AdminOperations:
    
    @staticmethod
    def create_admin(username, email, password_hash):
        try:
            if Admin.objects(email=email.lower()).first():
                raise AdminCreationError("Admin with this email already exists.")
                
            admin_id = str(uuid.uuid4())
            admin = Admin(
                admin_id=admin_id,
                username=username,
                email=email.lower(),
                password=password_hash,
                permissions=["view_users", "view_resumes", "manage_system"]
            )
            admin.save()
            return admin
        except Exception as e:
            raise AdminCreationError(f"Failed to create admin {e}")
    @staticmethod
    def get_admin_by_email(email):
        try:
            admin = Admin.objects(email=email.lower()).first()
            if not admin:
                raise AdminCreationError("Admin not found")
               return admin
        except Exception as e:
            raise AdminCreationError(f"failed to get admin: {e}")

    
    @staticmethod
    def get_all_users():
        try:
            return User.objects.all()
        except Exception as e:
            raise AdminCreationError(f"Failed to retrieve users: {e}")
            
    @staticmethod
    def get_all_resumes():
        try:
            return Resume.objects.all()
        except Exception as e:
            raise AdminCreationError(f"Failed to retrieve resumes: {e}")
