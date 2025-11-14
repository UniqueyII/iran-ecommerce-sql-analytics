# config/database_config.py

DATABASE_CONFIG = {
    'development': {
        'host': 'localhost',
        'database': 'Iran E-Commerce Analytics', 
        'user': 'postgres',
        'password': 'UniqueyA000#*&',
        'port': '5432'
    }
}

def test_connection():
    """Test database connection"""
    import psycopg2
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG['development'])
        print("✅ Database connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"📊 PostgreSQL version: {db_version[0]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure:")
        print("   • PostgreSQL is running")
        print("   • Database name is correct")
        print("   • Password is correct")
        print("   • PostgreSQL is on port 5432")
        return False

# Only run if this file is executed directly
if __name__ == "__main__":
    test_connection()

