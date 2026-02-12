#!/usr/bin/env python
"""
Script to automatically create PostgreSQL database for Django project
"""
import psycopg2
from psycopg2 import sql
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'maazith2005',
    'database': 'postgres'  # Connect to default 'postgres' database first
}

NEW_DATABASE = 'myshp_db'

def create_database():
    """Create the myshp_db database"""
    try:
        print(f"[*] Connecting to PostgreSQL as '{DB_CONFIG['user']}'...")
        
        # Connect to PostgreSQL server (using default 'postgres' database)
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True  # Required for creating databases
        
        cursor = conn.cursor()
        
        # Check if database already exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (NEW_DATABASE,)
        )
        
        if cursor.fetchone():
            print(f"[OK] Database '{NEW_DATABASE}' already exists!")
            cursor.close()
            conn.close()
            return True
        
        # Create database
        print(f"[*] Creating database '{NEW_DATABASE}'...")
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(NEW_DATABASE)
            )
        )
        
        print(f"[OK] Database '{NEW_DATABASE}' created successfully!")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Error connecting to PostgreSQL:")
        print(f"   {e}")
        print("\n[TIP] Troubleshooting:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check if password is correct: maazith2005")
        print("   3. Verify PostgreSQL is installed and accessible")
        return False
        
    except psycopg2.Error as e:
        print(f"[ERROR] Error creating database:")
        print(f"   {e}")
        return False
        
    except Exception as e:
        print(f"[ERROR] Unexpected error:")
        print(f"   {e}")
        return False

def test_connection():
    """Test connection to the new database"""
    try:
        print(f"\n[*] Testing connection to '{NEW_DATABASE}'...")
        
        test_config = DB_CONFIG.copy()
        test_config['database'] = NEW_DATABASE
        
        conn = psycopg2.connect(**test_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"[OK] Successfully connected to '{NEW_DATABASE}'!")
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error testing connection:")
        print(f"   {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("PostgreSQL Database Creation Script")
    print("=" * 60)
    print()
    
    if create_database():
        if test_connection():
            print("\n" + "=" * 60)
            print("[SUCCESS] Database is ready!")
            print("=" * 60)
            print("\n[Next Steps]")
            print("   1. Run: python manage.py migrate")
            print("   2. Run: python manage.py createsuperuser")
            print("   3. Run: python manage.py runserver")
            sys.exit(0)
        else:
            print("\n[WARNING] Database created but connection test failed.")
            sys.exit(1)
    else:
        print("\n[ERROR] Failed to create database.")
        sys.exit(1)

