# test_connection.py
import psycopg2

def debug_connection():
    print("🔍 Debugging database connection...")
    
    # Your connection details
    config = {
        'host': 'localhost',
        'database': 'Iran E-Commerce Analytics', 
        'user': 'postgres',
        'password': 'UniqueyA000#*&',
        'port': '5432'
    }
    
    try:
        print("1. Attempting to connect to PostgreSQL...")
        conn = psycopg2.connect(**config)
        print("✅ Connection successful!")
        
        # Test if database exists and has tables
        cursor = conn.cursor()
        
        print("2. Checking if database has tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("❌ No tables found in database")
            
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection error: {e}")
        print("\n💡 TROUBLESHOOTING:")
        print("   • Is PostgreSQL running?")
        print("   • Is the database name correct?")
        print("   • Check password and username")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    debug_connection()