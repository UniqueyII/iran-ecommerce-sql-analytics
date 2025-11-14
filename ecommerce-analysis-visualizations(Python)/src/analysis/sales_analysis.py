# src/analysis/sales_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../database'))
from connection import DatabaseConnection
from queries import ECommerceQueries

# Import font utilities
from font_utils import setup_persian_font, persian_text

class SalesAnalyzer:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.create_engine()
        setup_persian_font()
        
    def analyze_sales_performance(self):
        """Run complete sales performance analysis"""
        print("📈 Analyzing sales performance...")
        
        # Get data from database
        query = ECommerceQueries.sales_by_province()
        df = self.db.run_query(query)
        
        if df is not None:
            # Clean data and fix correlation issues
            df = self._clean_sales_data(df)
            self._create_sales_visualizations(df)
            self._generate_sales_insights(df)
            return df
        return None
    
    def _clean_sales_data(self, df):
        """Clean and prepare sales data"""
        # Clean province names
        if 'province' in df.columns:
            df['province'] = df['province'].apply(persian_text)
        
        # Ensure numeric columns are properly formatted and remove zeros/invalid values
        numeric_columns = ['total_sales', 'order_count', 'customer_count', 'avg_order_value']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Replace zeros with small values to avoid division issues
                df[col] = df[col].replace(0, 0.001)
        
        return df
    
    def _create_sales_visualizations(self, df):
        """Create professional sales visualizations with Persian support"""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        fig.suptitle('Sales Performance Dashboard', fontsize=16, fontweight='bold')
        
        # Get top provinces for better readability
        df_top_sales = df.nlargest(min(8, len(df)), 'total_sales').sort_values('total_sales', ascending=True)
        
        # 1. Total sales by province (horizontal bar)
        if len(df_top_sales) > 0:
            provinces = [str(p) for p in df_top_sales['province']]
            bars = axes[0,0].barh(provinces, df_top_sales['total_sales'] / 1000000, 
                                 color='#2980b9', alpha=0.8, edgecolor='black', linewidth=0.5)
            axes[0,0].set_xlabel('Total Sales (Million Tomans)', fontweight='bold')
            axes[0,0].set_title('Top Provinces by Sales', fontweight='bold', fontsize=12)
            axes[0,0].grid(True, alpha=0.3, axis='x')
            
            # Adjust font size for text
            axes[0,0].tick_params(axis='y', labelsize=9)
            
            # Add value labels on bars
            for bar in bars:
                width = bar.get_width()
                axes[0,0].text(width + 0.1, bar.get_y() + bar.get_height()/2,
                              f'{width:,.1f}M', va='center', fontweight='bold', fontsize=8)
        else:
            axes[0,0].text(0.5, 0.5, 'No sales data available', ha='center', va='center', 
                          transform=axes[0,0].transAxes, fontsize=12)
            axes[0,0].set_title('Top Provinces by Sales', fontweight='bold', fontsize=12)
        
        # 2. Order count by province
        df_orders = df.nlargest(min(6, len(df)), 'order_count')
        if len(df_orders) > 0:
            province_names = [str(p) for p in df_orders['province']]
            bars = axes[0,1].bar(province_names, df_orders['order_count'], 
                                color='#27ae60', alpha=0.8, edgecolor='black', linewidth=0.5)
            axes[0,1].set_ylabel('Number of Orders', fontweight='bold')
            axes[0,1].set_title('Top Provinces by Order Count', fontweight='bold', fontsize=12)
            axes[0,1].tick_params(axis='x', rotation=45, labelsize=9)
            axes[0,1].grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                axes[0,1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                              f'{height:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        else:
            axes[0,1].text(0.5, 0.5, 'No order data available', ha='center', va='center', 
                          transform=axes[0,1].transAxes, fontsize=12)
            axes[0,1].set_title('Top Provinces by Order Count', fontweight='bold', fontsize=12)
        
        # 3. Average order value
        df_aov = df.nlargest(min(6, len(df)), 'avg_order_value')
        if len(df_aov) > 0:
            province_names_aov = [str(p) for p in df_aov['province']]
            aov_thousands = df_aov['avg_order_value'] / 1000
            bars = axes[1,0].bar(province_names_aov, aov_thousands, 
                                color='#e67e22', alpha=0.8, edgecolor='black', linewidth=0.5)
            axes[1,0].set_ylabel('Average Order Value (Thousand Tomans)', fontweight='bold')
            axes[1,0].set_title('Top Provinces by Average Order Value', fontweight='bold', fontsize=12)
            axes[1,0].tick_params(axis='x', rotation=45, labelsize=9)
            axes[1,0].grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                axes[1,0].text(bar.get_x() + bar.get_width()/2., height + max(aov_thousands)*0.01,
                              f'{height:,.0f}K', ha='center', va='bottom', fontweight='bold', fontsize=8)
        else:
            axes[1,0].text(0.5, 0.5, 'No AOV data available', ha='center', va='center', 
                          transform=axes[1,0].transAxes, fontsize=12)
            axes[1,0].set_title('Top Provinces by Average Order Value', fontweight='bold', fontsize=12)
        
        # 4. Customer count vs Sales scatter
        valid_data = df[(df['customer_count'] > 0) & (df['total_sales'] > 0)]
        if len(valid_data) > 1:
            scatter = axes[1,1].scatter(valid_data['customer_count'], valid_data['total_sales'] / 1000000, 
                                       s=80, alpha=0.7, color='#9b59b6', edgecolors='black', linewidth=0.5)
            axes[1,1].set_xlabel('Number of Customers', fontweight='bold')
            axes[1,1].set_ylabel('Total Sales (Million Tomans)', fontweight='bold')
            axes[1,1].set_title('Customer Count vs Sales Revenue', fontweight='bold', fontsize=12)
            axes[1,1].grid(True, alpha=0.3)
            
            # Add province labels for top performers only
            top_performers = valid_data.nlargest(min(3, len(valid_data)), 'total_sales')
            for i, row in top_performers.iterrows():
                province_name = str(row['province'])
                axes[1,1].annotate(province_name, 
                                  (row['customer_count'], row['total_sales'] / 1000000),
                                  xytext=(8, 8), textcoords='offset points', 
                                  fontsize=8, fontweight='bold',
                                  bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
            
            # Calculate and display correlation
            correlation = valid_data['customer_count'].corr(valid_data['total_sales'])
            correlation_text = f'Correlation: {correlation:.2f}' if not pd.isna(correlation) else 'Correlation: N/A'
            
            axes[1,1].text(0.05, 0.95, correlation_text, 
                          transform=axes[1,1].transAxes, fontsize=11, fontweight='bold',
                          bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
        else:
            axes[1,1].text(0.5, 0.5, 'Insufficient data for correlation', ha='center', va='center', 
                          transform=axes[1,1].transAxes, fontsize=12)
            axes[1,1].set_title('Customer Count vs Sales Revenue', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        
        # Save the figure - FIXED: Ensure proper saving
        os.makedirs('outputs/images', exist_ok=True)
        output_path = 'outputs/images/sales_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ Chart saved to: {output_path}")
        plt.show()
    
    def _generate_sales_insights(self, df):
        """Generate sales insights"""
        print("\n📈 SALES ANALYSIS INSIGHTS:")
        print("=" * 50)
        
        total_sales = df['total_sales'].sum()
        if len(df) > 0:
            top_province = df.loc[df['total_sales'].idxmax()]
            avg_order_value = df['avg_order_value'].mean()
        else:
            top_province = {'province': 'N/A', 'total_sales': 0}
            avg_order_value = 0
        
        # Fix correlation calculation
        valid_data = df[(df['customer_count'] > 0) & (df['total_sales'] > 0)]
        if len(valid_data) > 1:
            correlation = valid_data['customer_count'].corr(valid_data['total_sales'])
        else:
            correlation = float('nan')
        
        print(f"• Total Sales: {total_sales/1000000:,.1f} Million Tomans")
        print(f"• Top Performing Province: {top_province['province']}")
        print(f"• Sales in Top Province: {top_province['total_sales']/1000000:,.1f}M Tomans")
        print(f"• Average Order Value: {avg_order_value/1000:,.0f} Thousand Tomans")
        print(f"• Number of Active Provinces: {len(df)}")
        print(f"• Total Orders: {df['order_count'].sum():,}")
        print(f"• Customer-Sales Correlation: {correlation:.2f}")
        
    def close(self):
        """Close database connection"""
        self.db.close()