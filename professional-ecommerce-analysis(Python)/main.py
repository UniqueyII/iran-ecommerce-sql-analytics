# main.py - PROFESSIONAL E-COMMERCE ANALYSIS

import os
import sys
import traceback

print("🚀 STARTING PROFESSIONAL E-COMMERCE ANALYSIS")
print("=" * 50)

# Add the correct paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src', 'analysis'))
sys.path.insert(0, os.path.join(current_dir, 'src', 'database'))

try:
    # Try to import our custom modules
    from customer_analysis import CustomerAnalyzer
    from sales_analysis import SalesAnalyzer
    print("✅ All analysis modules imported successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Debugging import paths...")
    
    # Show what files exist
    analysis_path = os.path.join(current_dir, 'src', 'analysis')
    if os.path.exists(analysis_path):
        print(f"📁 Files in analysis folder: {os.listdir(analysis_path)}")
    else:
        print(f"❌ Analysis folder not found at: {analysis_path}")
    
    database_path = os.path.join(current_dir, 'src', 'database')
    if os.path.exists(database_path):
        print(f"📁 Files in database folder: {os.listdir(database_path)}")
    else:
        print(f"❌ Database folder not found at: {database_path}")
    
    sys.exit(1)

def run_customer_analysis():
    """Run customer churn analysis"""
    print("\n" + "="*50)
    print("1. CUSTOMER CHURN ANALYSIS")
    print("="*50)
    
    try:
        analyzer = CustomerAnalyzer()
        data = analyzer.analyze_customer_churn()
        analyzer.close()
        return data
    except Exception as e:
        print(f"❌ Customer analysis failed: {e}")
        traceback.print_exc()
        return None

def run_sales_analysis():
    """Run sales performance analysis"""
    print("\n" + "="*50)
    print("2. SALES PERFORMANCE ANALYSIS") 
    print("="*50)
    
    try:
        analyzer = SalesAnalyzer()
        data = analyzer.analyze_sales_performance()
        analyzer.close()
        return data
    except Exception as e:
        print(f"❌ Sales analysis failed: {e}")
        traceback.print_exc()
        return None

def main():
    """Main analysis function"""
    try:
        # Run both analyses
        customer_data = run_customer_analysis()
        sales_data = run_sales_analysis()
        
        # Summary
        print("\n" + "="*50)
        print("📊 ANALYSIS SUMMARY")
        print("="*50)
        
        if customer_data is not None and sales_data is not None:
            print("✅ ALL ANALYSES COMPLETED SUCCESSFULLY!")
            print("\n📁 Generated Reports:")
            print("   • outputs/images/customer_churn_analysis.png")
            print("   • outputs/images/sales_analysis.png")
            print("\n🎯 Business Insights Available!")
        else:
            print("❌ Some analyses failed - check errors above")
            
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("\n" + "🎉" * 20)
    print("PROFESSIONAL ANALYSIS COMPLETE!")
    print("🎉" * 20)