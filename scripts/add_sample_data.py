#!/usr/bin/env python3
"""
Script to add sample data to the database for testing
"""
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import get_db_connection

def add_sample_data():
    """Add sample users and profiles to the database"""
    db = get_db_connection()
    
    try:
        # Add sample users
        users_data = [
            ('user1', 'testuser1', 'user1@example.com'),
            ('user2', 'testuser2', 'user2@example.com'),
        ]
        
        for user_id, username, email in users_data:
            try:
                query = """
                INSERT INTO users (user_id, username, email, created_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
                """
                db.execute_query(query, (user_id, username, email, datetime.now()))
                print(f"✅ Added user: {user_id}")
            except Exception as e:
                print(f"⚠️  User {user_id} already exists or error: {e}")
        
        # Add sample profiles
        profiles_data = [
            {
                'profile_id': 'profile1',
                'user_id': 'user1',
                'profile_name': 'Sales Data Analysis',
                'data_sources': json.dumps([
                    {
                        'url': 'file://sample_data/sales.csv',
                        'filename': 'sales.csv',
                        'description': 'Sales data for analysis'
                    },
                    {
                        'url': 'file://sample_data/regions.csv',
                        'filename': 'regions.csv',
                        'description': 'Regional sales data'
                    },
                    {
                        'url': 'file://sample_data/products.csv',
                        'filename': 'products.csv',
                        'description': 'Product catalog and pricing'
                    }
                ]),
                'is_active': True
            },
            {
                'profile_id': 'profile2',
                'user_id': 'user1',
                'profile_name': 'Customer Analytics',
                'data_sources': json.dumps([
                    {
                        'url': 'file://sample_data/customers.csv',
                        'filename': 'customers.csv',
                        'description': 'Customer demographic data'
                    },
                    {
                        'url': 'file://sample_data/purchases.csv',
                        'filename': 'purchases.csv',
                        'description': 'Customer purchase history'
                    },
                    {
                        'url': 'file://sample_data/feedback.csv',
                        'filename': 'feedback.csv',
                        'description': 'Customer feedback and ratings'
                    },
                    {
                        'url': 'file://sample_data/support.csv',
                        'filename': 'support.csv',
                        'description': 'Customer support tickets'
                    }
                ]),
                'is_active': True
            },
            {
                'profile_id': 'profile3',
                'user_id': 'user2',
                'profile_name': 'Financial Reports',
                'data_sources': json.dumps([
                    {
                        'url': 'file://sample_data/financial.csv',
                        'filename': 'financial.csv',
                        'description': 'Financial performance data'
                    },
                    {
                        'url': 'https://raw.githubusercontent.com/datasets/financial-data/main/budget.csv',
                        'filename': 'budget.csv',
                        'description': 'Budget planning and forecasts'
                    },
                    {
                        'url': 'https://raw.githubusercontent.com/datasets/financial-data/main/expenses.csv',
                        'filename': 'expenses.csv',
                        'description': 'Expense tracking and categorization'
                    }
                ]),
                'is_active': True
            }
        ]
        
        for profile in profiles_data:
            try:
                query = """
                INSERT INTO user_profiles (profile_id, user_id, profile_name, data_sources, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (profile_id) DO NOTHING
                """
                db.execute_query(query, (
                    profile['profile_id'],
                    profile['user_id'],
                    profile['profile_name'],
                    profile['data_sources'],
                    profile['is_active'],
                    datetime.now()
                ))
                print(f"✅ Added profile: {profile['profile_name']} for user {profile['user_id']}")
            except Exception as e:
                print(f"⚠️  Profile {profile['profile_id']} already exists or error: {e}")
        
        print("\n🎉 Sample data added successfully!")
        print("\nYou can now test the application with:")
        print("- User ID: user1 (has 2 profiles)")
        print("- User ID: user2 (has 1 profile)")
        
    except Exception as e:
        print(f"❌ Failed to add sample data: {e}")
        raise

if __name__ == "__main__":
    add_sample_data()
