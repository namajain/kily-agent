"""
Database configuration and connection utilities for MVP
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration class"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'qna_agent')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'password')
        
    def get_connection_string(self):
        """Get database connection string"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_connection_params(self):
        """Get database connection parameters"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }

class DatabaseConnection:
    """Database connection manager"""
    
    def __init__(self, config: DatabaseConfig = None):
        self.config = config or DatabaseConfig()
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(
                **self.config.get_connection_params(),
                cursor_factory=RealDictCursor
            )
            logger.info("Database connection established")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return results"""
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            return result
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def execute_many(self, query: str, params_list: list):
        """Execute multiple queries with different parameters"""
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            result = cursor.rowcount
            cursor.close()
            return result
            
        except Exception as e:
            logger.error(f"Batch query execution failed: {e}")
            if self.connection:
                self.connection.rollback()
            raise

# Global database instance
db_config = DatabaseConfig()
db_connection = DatabaseConnection(db_config)

def get_db_connection():
    """Get database connection instance"""
    return db_connection

def init_database():
    """Initialize database with schema"""
    try:
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        # Execute schema
        db_connection.execute_query(schema)
        logger.info("Database schema initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise 