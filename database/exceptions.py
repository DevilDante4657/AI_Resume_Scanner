class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class UserNotFoundError(DatabaseError):
    """User not found in database"""
    pass

class ResumeNotFoundError(DatabaseError):
    """Resume not found in database"""
    pass

class ResumeCreationError(DatabaseError):
    """Failed to create resume"""
    pass

class KeywordCreationError(DatabaseError):
    """Failed to create or find keywords"""
    pass

class AdminCreationError(DatabaseError):
    """Failed to create or find admin"""
    pass

class AnalysisUpdateError(DatabaseError):
    """Failed to update analysis"""
    pass
