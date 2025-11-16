from database.connection import get_db_connection
from database.models import User
import uuid
import bcrypt

def test_connection():
    print("=" * 50)
    print("Testing MongoDB Connection")
    print("=" * 50)
    try:
        db = get_db_connection()
        print(" Database connection successful!\n")
        return True
    except Exception as e:
        print(f" Database connection failed: {e}\n")
        return False

def test_create_user():
    print("Testing User Creation")
    print("-" * 50)
    try:
        password = "testpass123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(
            user_id=str(uuid.uuid4()),
            username="testuser",
            email="test@example.com",
            password=password_hash
        )
        user.save()
        
        print(" User created successfully!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   User ID: {user.user_id}\n")
        return user
    except Exception as e:
        print(f" User creation failed: {e}\n")
        return None

def run_tests():
    print("\n" + "=" * 50)
    print("MONGODB DATABASE TESTS")
    print("=" * 50 + "\n")
    
    if not test_connection():
        return
    
    user = test_create_user()
    
    if user:
        print("=" * 50)
        print(" ALL TESTS PASSED!")
        print("=" * 50)
        print("\nYour database is working!")
    else:
        print("=" * 50)
        print(" SOME TESTS FAILED")
        print("=" * 50)

if __name__ == "__main__":
    run_tests()