# src/analysis/customer_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add database to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../database'))
from connection import DatabaseConnection
from queries import ECommerceQueries

# Import font utilities
from font_utils import setup_persian_font, persian_text

class CustomerAnalyzer:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.create_engine()
        setup_persian_font()
        
    def analyze_customer_churn(self):
        """Run complete customer churn analysis"""
        print("🔍 Analyzing customer churn...")
        
        # Get data from database
        query = ECommerceQueries.customer_churn_analysis()
        df = self.db.run_query(query)
        
        if df is not None:
            # Clean Persian text in dataframe
            if 'province' in df.columns:
                df['province'] = df['province'].apply(persian_text)
            self._create_visualizations(df)
            self._generate_insights(df)
            return df
        return None
    
    def _create_visualizations(self, df):
        """Create professional visualizations with Persian support"""
        # Set professional style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Customer Churn Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # Define consistent color scheme
        risk_colors = {'High Risk': '#e74c3c', 'Medium Risk': '#f39c12', 'Low Risk': '#2ecc71'}
        
        # 1. Risk distribution pie chart
        risk_counts = df['risk_level'].value_counts()
        colors = [risk_colors.get(risk, '#95a5a6') for risk in risk_counts.index]
        wedges, texts, autotexts = axes[0,0].pie(risk_counts.values, labels=risk_counts.index, 
                                                autopct='%1.1f%%', startangle=90, colors=colors)
        axes[0,0].set_title('Customer Risk Distribution', fontweight='bold', fontsize=12)
        # Make percentages bold
        for autotext in autotexts:
            autotext.set_fontweight('bold')
        
        # 2. Revenue by risk level
        revenue_by_risk = df.groupby('risk_level')['total_spent'].sum().sort_values(ascending=True)
        revenue_millions = revenue_by_risk.values / 1000000
        bars = axes[0,1].barh(list(revenue_by_risk.index), revenue_millions, 
                             color=[risk_colors.get(risk, '#95a5a6') for risk in revenue_by_risk.index],
                             alpha=0.8)
        axes[0,1].set_xlabel('Revenue (Million Tomans)', fontweight='bold')
        axes[0,1].set_title('Revenue at Risk by Customer Segment', fontweight='bold', fontsize=12)
        axes[0,1].grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for bar, value in zip(bars, revenue_millions):
            width = bar.get_width()
            axes[0,1].text(width + max(revenue_millions)*0.01, bar.get_y() + bar.get_height()/2,
                          f'{value:,.1f}M', va='center', fontweight='bold')
        
        # 3. Days since last purchase histogram
        active_customers = df[df['days_since_last_purchase'] < 365]
        if len(active_customers) > 0:
            axes[1,0].hist(active_customers['days_since_last_purchase'], bins=15, 
                          alpha=0.7, color='#3498db', edgecolor='black', linewidth=0.5)
            axes[1,0].set_xlabel('Days Since Last Purchase', fontweight='bold')
            axes[1,0].set_ylabel('Number of Customers', fontweight='bold')
            axes[1,0].set_title('Customer Activity Distribution', fontweight='bold', fontsize=12)
            axes[1,0].grid(True, alpha=0.3)
        else:
            axes[1,0].text(0.5, 0.5, 'No active customer data', ha='center', va='center', 
                          transform=axes[1,0].transAxes, fontsize=12)
            axes[1,0].set_title('Customer Activity Distribution', fontweight='bold', fontsize=12)
        
        # 4. Orders vs Revenue scatter
        scatter = axes[1,1].scatter(df['order_count'], df['total_spent'] / 1000000, 
                                   c=df['days_since_last_purchase'], cmap='viridis', 
                                   alpha=0.7, s=60, edgecolors='black', linewidth=0.5)
        axes[1,1].set_xlabel('Number of Orders', fontweight='bold')
        axes[1,1].set_ylabel('Total Revenue (Million Tomans)', fontweight='bold')
        axes[1,1].set_title('Customer Value vs Activity', fontweight='bold', fontsize=12)
        axes[1,1].grid(True, alpha=0.3)
        
        # Add colorbar for days since last purchase
        cbar = plt.colorbar(scatter, ax=axes[1,1])
        cbar.set_label('Days Since Last Purchase', fontweight='bold')
        
        plt.tight_layout()
        
        # Save the figure - FIXED: Ensure directory exists and save properly
        os.makedirs('outputs/images', exist_ok=True)
        output_path = 'outputs/images/customer_churn_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ Chart saved to: {output_path}")
        plt.show()
    
    def _generate_insights(self, df):
        """Generate business insights"""
        print("\n📊 CUSTOMER ANALYSIS INSIGHTS:")
        print("=" * 50)
        
        total_customers = len(df)
        high_risk = len(df[df['risk_level'] == 'High Risk'])
        medium_risk = len(df[df['risk_level'] == 'Medium Risk'])
        total_revenue_at_risk = df[df['risk_level'].isin(['High Risk', 'Medium Risk'])]['total_spent'].sum()
        avg_order_value = df['total_spent'].mean()
        
        # Handle Persian province names
        most_active_province = df['province'].mode().iloc[0] if not df['province'].mode().empty else 'N/A'
        
        print(f"• Total Customers: {total_customers:,}")
        print(f"• High-Risk Customers: {high_risk} ({high_risk/total_customers*100:.1f}%)")
        print(f"• Medium-Risk Customers: {medium_risk} ({medium_risk/total_customers*100:.1f}%)")
        print(f"• Revenue at Risk: {total_revenue_at_risk/1000000:,.1f} Million Tomans")
        print(f"• Average Customer Value: {avg_order_value/1000:,.0f} Thousand Tomans")
        print(f"• Most Active Province: {most_active_province}")
        
    def close(self):
        """Close database connection"""
        self.db.close()