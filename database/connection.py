from mongoengine import connect, disconnect

class DatabaseConnection:
    
    def __init__(self, db_name="resumeScanner", host="localhost", port=27017):
        self.db_name = db_name
        self.host = host
        self.port = port
        self.connection = None
    
    def connect_db(self):
        try:
            self.connection = connect(
                db=self.db_name,
                host=self.host,
                port=self.port
            )
            print(f" Connected to MongoDB: {self.db_name}")
            return self.connection
        except Exception as e:
            print(f" Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect_db(self):
        disconnect()
        print("Disconnected from MongoDB")

def get_db_connection():
    db = DatabaseConnection()
    db.connect_db()
    return db