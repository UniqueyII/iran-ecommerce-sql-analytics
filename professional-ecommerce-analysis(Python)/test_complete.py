# test_complete.py
import sys
import os

print("🔍 TESTING COMPLETE SETUP")
print("=" * 40)

# Add paths
current_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_dir, 'src', 'analysis'))
sys.path.insert(0, os.path.join(current_dir, 'src', 'database'))

# Test database connection first
print("\n1. Testing database connection...")
try:
    from database_config import test_connection
    if test_connection():
        print("✅ Database connection: PASS")
    else:
        print("❌ Database connection: FAIL")
        sys.exit(1)
except Exception as e:
    print(f"❌ Database config: {e}")
    sys.exit(1)

# Test imports
print("\n2. Testing module imports...")
modules_to_test = [
    ('customer_analysis', 'CustomerAnalyzer'),
    ('sales_analysis', 'SalesAnalyzer'),
    ('connection', 'DatabaseConnection'),
    ('queries', 'ECommerceQueries')
]

all_imports_ok = True
for module_name, class_name in modules_to_test:
    try:
        if module_name == 'customer_analysis':
            from customer_analysis import CustomerAnalyzer
        elif module_name == 'sales_analysis':
            from sales_analysis import SalesAnalyzer
        elif module_name == 'connection':
            from connection import DatabaseConnection
        elif module_name == 'queries':
            from queries import ECommerceQueries
        print(f"✅ {module_name}.{class_name}: IMPORTED")
    except Exception as e:
        print(f"❌ {module_name}.{class_name}: {e}")
        all_imports_ok = False

if all_imports_ok:
    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
    print("🚀 Ready to run main analysis!")
else:
    print("\n💥 SOME IMPORTS FAILED!")
    print("Check the errors above.")