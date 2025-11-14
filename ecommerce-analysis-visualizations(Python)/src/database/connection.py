# src/database/connection.py

import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import sys
import os

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../config'))
from database_config import DATABASE_CONFIG

class DatabaseConnection:
    def __init__(self, environment='development'):
        self.config = DATABASE_CONFIG[environment]
        self.connection = None
        self.engine = None
        
    def connect(self):
        """Create direct PostgreSQL connection"""
        try:
            self.connection = psycopg2.connect(**self.config)
            print("✅ PostgreSQL connection established")
            return self.connection
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None
            
    def create_engine(self):
        """Create SQLAlchemy engine for pandas"""
        try:
            connection_string = f"postgresql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            self.engine = create_engine(connection_string)
            print("✅ SQLAlchemy engine created")
            return self.engine
        except Exception as e:
            print(f"❌ Engine creation failed: {e}")
            return None
            
    def run_query(self, query):
        """Execute SQL query and return DataFrame"""
        try:
            if self.engine is None:
                self.create_engine()
            df = pd.read_sql(query, self.engine)
            print(f"✅ Query executed successfully. Returned {len(df)} rows")
            return df
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return None
            
    def close(self):
        """Close connections"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        print("🔒 Connections closed")