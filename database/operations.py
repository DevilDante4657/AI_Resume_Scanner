from database.models import (
    User, Resume, Admin, KeywordsUserInput, 
    MLModel, UpdatedResume, UserFile, AnalysisResult
)
from datetime import datetime
import uuid

from database.exceptions import (
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
            raise AdminCreationError(f"Failed to create user: {e}")
    
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
