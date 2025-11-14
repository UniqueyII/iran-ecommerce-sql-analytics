# test_real_connection.py
import sys
import os

# Add paths
current_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_dir, 'src', 'analysis'))
sys.path.insert(0, os.path.join(current_dir, 'src', 'database'))

from customer_analysis import CustomerAnalyzer

print("🔗 TESTING REAL DATABASE CONNECTION")
print("=" * 40)

try:
    # Create analyzer - this will connect to your REAL database
    analyzer = CustomerAnalyzer()
    
    # Test a real query
    print("📊 Running real SQL query on your database...")
    from queries import ECommerceQueries
    query = ECommerceQueries.customer_churn_analysis()
    
    # This executes against your ACTUAL "Iran E-Commerce Analytics" database
    df = analyzer.db.run_query(query)
    
    if df is not None:
        print(f"✅ SUCCESS! Connected to REAL database!")
        print(f"📊 Retrieved {len(df)} customer records from your SQL tables")
        print(f"🔍 First few records:")
        print(df.head(3))  # Show actual data from your database
    else:
        print("❌ Failed to get data from database")
        
    analyzer.close()
    
except Exception as e:
    print(f"❌ Connection test failed: {e}")
    import traceback
    traceback.print_exc()