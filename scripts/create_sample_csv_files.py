#!/usr/bin/env python3
"""
Script to create sample CSV files for testing
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_csv_files():
    """Create sample CSV files for testing"""
    
    # Create data directory
    data_dir = "sample_data"
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Sales Data
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    sales_data = {
        'date': np.random.choice(dates, 1000),
        'product_id': np.random.randint(1, 101, 1000),
        'quantity': np.random.randint(1, 50, 1000),
        'unit_price': np.random.uniform(10, 500, 1000),
        'customer_id': np.random.randint(1, 1001, 1000),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 1000)
    }
    
    sales_df = pd.DataFrame(sales_data)
    sales_df['total_amount'] = sales_df['quantity'] * sales_df['unit_price']
    sales_df.to_csv(f"{data_dir}/sales.csv", index=False)
    print(f"✅ Created {data_dir}/sales.csv")
    
    # 2. Regions Data
    regions_data = {
        'region_id': [1, 2, 3, 4],
        'region_name': ['North', 'South', 'East', 'West'],
        'manager': ['John Smith', 'Jane Doe', 'Bob Johnson', 'Alice Brown'],
        'target_sales': [1000000, 1200000, 900000, 1100000]
    }
    
    regions_df = pd.DataFrame(regions_data)
    regions_df.to_csv(f"{data_dir}/regions.csv", index=False)
    print(f"✅ Created {data_dir}/regions.csv")
    
    # 3. Products Data
    products_data = {
        'product_id': range(1, 101),
        'product_name': [f'Product_{i}' for i in range(1, 101)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 100),
        'price': np.random.uniform(10, 500, 100),
        'stock_quantity': np.random.randint(0, 1000, 100)
    }
    
    products_df = pd.DataFrame(products_data)
    products_df.to_csv(f"{data_dir}/products.csv", index=False)
    print(f"✅ Created {data_dir}/products.csv")
    
    # 4. Customer Data
    customer_data = {
        'customer_id': range(1, 1001),
        'name': [f'Customer_{i}' for i in range(1, 1001)],
        'email': [f'customer{i}@example.com' for i in range(1, 1001)],
        'age': np.random.randint(18, 80, 1000),
        'gender': np.random.choice(['M', 'F'], 1000),
        'income_level': np.random.choice(['Low', 'Medium', 'High'], 1000),
        'registration_date': np.random.choice(dates, 1000)
    }
    
    customer_df = pd.DataFrame(customer_data)
    customer_df.to_csv(f"{data_dir}/customers.csv", index=False)
    print(f"✅ Created {data_dir}/customers.csv")
    
    # 5. Purchases Data
    purchases_data = {
        'purchase_id': range(1, 2001),
        'customer_id': np.random.randint(1, 1001, 2000),
        'product_id': np.random.randint(1, 101, 2000),
        'purchase_date': np.random.choice(dates, 2000),
        'amount': np.random.uniform(10, 1000, 2000),
        'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'Cash', 'PayPal'], 2000)
    }
    
    purchases_df = pd.DataFrame(purchases_data)
    purchases_df.to_csv(f"{data_dir}/purchases.csv", index=False)
    print(f"✅ Created {data_dir}/purchases.csv")
    
    # 6. Feedback Data
    feedback_data = {
        'feedback_id': range(1, 501),
        'customer_id': np.random.randint(1, 1001, 500),
        'product_id': np.random.randint(1, 101, 500),
        'rating': np.random.randint(1, 6, 500),
        'comment': [f'Feedback comment {i}' for i in range(1, 501)],
        'feedback_date': np.random.choice(dates, 500)
    }
    
    feedback_df = pd.DataFrame(feedback_data)
    feedback_df.to_csv(f"{data_dir}/feedback.csv", index=False)
    print(f"✅ Created {data_dir}/feedback.csv")
    
    # 7. Support Data
    support_data = {
        'ticket_id': range(1, 301),
        'customer_id': np.random.randint(1, 1001, 300),
        'issue_type': np.random.choice(['Technical', 'Billing', 'Product', 'General'], 300),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 300),
        'status': np.random.choice(['Open', 'In Progress', 'Resolved', 'Closed'], 300),
        'created_date': np.random.choice(dates, 300),
        'resolution_time_hours': np.random.randint(1, 72, 300)
    }
    
    support_df = pd.DataFrame(support_data)
    support_df.to_csv(f"{data_dir}/support.csv", index=False)
    print(f"✅ Created {data_dir}/support.csv")
    
    # 8. Financial Data
    financial_data = {
        'date': pd.date_range(start='2024-01-01', end='2024-12-31', freq='M'),
        'revenue': np.random.uniform(50000, 200000, 12),
        'expenses': np.random.uniform(30000, 150000, 12),
        'profit': np.random.uniform(10000, 80000, 12),
        'cash_flow': np.random.uniform(-50000, 100000, 12),
        'assets': np.random.uniform(500000, 2000000, 12),
        'liabilities': np.random.uniform(200000, 1000000, 12)
    }
    
    financial_df = pd.DataFrame(financial_data)
    financial_df.to_csv(f"{data_dir}/financial.csv", index=False)
    print(f"✅ Created {data_dir}/financial.csv")
    
    print(f"\n🎉 All sample CSV files created in {data_dir}/ directory!")
    print("Files created:")
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            print(f"  - {file}")

if __name__ == "__main__":
    create_sample_csv_files()
