from mongoengine import (
    Document, EmbeddedDocument,
    StringField, IntField, FloatField, DateTimeField,
    ListField, DictField, BooleanField,
    ReferenceField, EmbeddedDocumentField
)
from datetime import datetime

# Embedded Documents

class Subscription(EmbeddedDocument):
    type = StringField(default="free", choices=["free", "premium"])
    scans_remaining = IntField(default=5)
    reset_date = DateTimeField()

class KeywordData(EmbeddedDocument):
    keyword = StringField(required=True)
    importance = IntField(min_value=1, max_value=10, default=5)
    found_in_resume = BooleanField(default=False)

class AnalysisResult(EmbeddedDocument):
    keywords_found = ListField(StringField())
    keywords_missing = ListField(StringField())
    keyword_density = DictField()
    has_contact_info = BooleanField(default=False)
    has_experience = BooleanField(default=False)
    has_education = BooleanField(default=False)
    has_skills = BooleanField(default=False)
    is_ats_friendly = BooleanField(default=False)
    formatting_issues = ListField(StringField())
    feedback = StringField()
    suggestions = ListField(StringField())

# Main Collections

class User(Document):
    user_id = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    last_login = DateTimeField()
    account_type = StringField(choices=["candidate", "admin"], default="candidate")
    subscription = EmbeddedDocumentField(Subscription, default=Subscription)
    
    meta = {
        'collection': 'users',
        'indexes': ['user_id', 'email', 'username']
    }

class Resume(Document):
    resume_id = StringField(required=True, unique=True)
    user_id = ReferenceField(User, required=True)
    file_name = StringField(required=True)
    file_type = StringField(choices=["pdf", "docx", "doc", "jpg", "jpeg"])
    upload_date = DateTimeField(default=datetime.now)
    file_url = StringField()
    original_text = StringField()
    status = StringField(choices=["pending", "processing", "completed", "failed"], default="pending")
    overall_score = IntField(min_value=0, max_value=100)
    scan_date = DateTimeField()
    analysis = EmbeddedDocumentField(AnalysisResult)
    
    meta = {
        'collection': 'resumes',
        'indexes': ['user_id', 'upload_date', 'status']
    }

class Admin(Document):
    admin_id = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.now)
    last_login = DateTimeField()
    permissions = ListField(StringField())
    
    meta = {
        'collection': 'admins',
        'indexes': ['email', 'username']
    }

class KeywordsUserInput(Document):
    keyword_id = StringField(required=True, unique=True)
    keywords = ListField(StringField())
    industry = StringField()
    job_role = StringField()
    job_description = StringField()
    created_at = DateTimeField(default=datetime.now)
    created_by = ReferenceField(User)
    
    meta = {
        'collection': 'keywords_user_input',
        'indexes': ['created_by', 'industry']
    }

class MLModel(Document):
    resume_id = ReferenceField(Resume, required=True)
    keyword_id = ReferenceField(KeywordsUserInput)
    model_version = StringField(default="v1.0")
    execution_date = DateTimeField(default=datetime.now)
    processing_time = FloatField()
    score = IntField(min_value=0, max_value=100)
    score_id = StringField()
    feedback = StringField()
    
    meta = {
        'collection': 'ml_model_results',
        'indexes': ['resume_id', 'execution_date']
    }

class UpdatedResume(Document):
    resume_id = StringField(required=True, unique=True)
    original_resume_id = ReferenceField(Resume, required=True)
    updated_text = StringField()
    updated_file_url = StringField()
    changes_made = ListField(StringField())
    improvement_score = IntField()
    created_at = DateTimeField(default=datetime.now)
    created_by = StringField()
    
    meta = {
        'collection': 'updated_resumes',
        'indexes': ['original_resume_id', 'created_at']
    }

class UserFile(Document):
    user_id = ReferenceField(User, required=True)
    login_count = IntField(default=0)
    login_history = ListField(DateTimeField())
    account_created = DateTimeField(default=datetime.now)
    subscription_type = StringField(default="free")
    scans_remaining = IntField(default=5)
    
    meta = {
        'collection': 'user_files',
        'indexes': ['user_id']
    }