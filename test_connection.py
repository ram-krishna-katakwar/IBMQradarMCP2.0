#!/usr/bin/env python3
"""Test script to verify QRadar connection"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test connection to QRadar"""
    
    # Import after loading env
    try:
        from src.qradar_client import QRadarClient
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure to install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    # Get configuration
    host = os.getenv("QRADAR_HOST")
    token = os.getenv("QRADAR_API_TOKEN")
    verify_ssl = os.getenv("QRADAR_VERIFY_SSL", "true").lower() == "true"
    
    # Validate configuration
    if not host:
        print("❌ QRADAR_HOST not set in .env file")
        sys.exit(1)
    
    if not token:
        print("❌ QRADAR_API_TOKEN not set in .env file")
        sys.exit(1)
    
    print("=" * 60)
    print("IBM QRadar MCP - Connection Test")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"SSL Verification: {verify_ssl}")
    print("=" * 60)
    print()
    
    # Test connection
    print("Testing connection...")
    try:
        client = QRadarClient(host, token, verify_ssl)
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        sys.exit(1)
    
    # Test system info API call
    print("\nFetching system information...")
    system_info_available = False
    try:
        info = client.get_system_info()
        print("✅ Successfully connected to QRadar!")
        print()
        print("QRadar Information:")
        print("-" * 60)
        print(f"Version: {info.get('external_version', 'Unknown')}")
        print(f"Release: {info.get('release_name', 'Unknown')}")
        print(f"Console Hostname: {info.get('console_hostname', 'Unknown')}")
        print("-" * 60)
        system_info_available = True
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg or "insufficient capabilities" in error_msg.lower():
            print("⚠️  System information endpoint requires additional permissions")
            print("    This is OK - trying alternative endpoints...")
        else:
            print(f"❌ Failed to connect to QRadar: {e}")
            print("\nTroubleshooting tips:")
            print("1. Verify QRADAR_HOST is correct (no https:// prefix)")
            print("2. Verify QRADAR_API_TOKEN is valid")
            print("3. Check network connectivity to QRadar")
            print("4. Try setting QRADAR_VERIFY_SSL=false for testing")
            sys.exit(1)
    
    # Test basic queries
    print("\nTesting API endpoints with your token permissions...")
    successful_tests = 0
    total_tests = 0
    
    # Test log sources
    print("\n1. Testing log sources endpoint...")
    total_tests += 1
    try:
        log_sources = client.get_log_sources()
        count = len(log_sources) if isinstance(log_sources, list) else 1
        print(f"   ✅ Log sources accessible - Found {count} log source(s)")
        successful_tests += 1
    except Exception as e:
        if "403" in str(e) or "insufficient" in str(e).lower():
            print(f"   ⚠️  No permission for log sources endpoint")
        else:
            print(f"   ❌ Error: {str(e)[:100]}")
    
    # Test offenses
    print("\n2. Testing offenses endpoint...")
    total_tests += 1
    try:
        offenses = client.get_offenses(range_header="0-4")
        count = len(offenses) if isinstance(offenses, list) else 1
        print(f"   ✅ Offenses accessible - Found {count} offense(s)")
        successful_tests += 1
    except Exception as e:
        if "403" in str(e) or "insufficient" in str(e).lower():
            print(f"   ⚠️  No permission for offenses endpoint")
        else:
            print(f"   ❌ Error: {str(e)[:100]}")
    
    # Test assets
    print("\n3. Testing assets endpoint...")
    total_tests += 1
    try:
        assets = client.get_assets()
        count = len(assets) if isinstance(assets, list) else 1
        print(f"   ✅ Assets accessible - Found {count} asset(s)")
        successful_tests += 1
    except Exception as e:
        if "403" in str(e) or "insufficient" in str(e).lower():
            print(f"   ⚠️  No permission for assets endpoint")
        else:
            print(f"   ❌ Error: {str(e)[:100]}")
    
    # Test rules
    print("\n4. Testing rules endpoint...")
    total_tests += 1
    try:
        rules = client.get_rules()
        count = len(rules) if isinstance(rules, list) else 1
        print(f"   ✅ Rules accessible - Found {count} rule(s)")
        successful_tests += 1
    except Exception as e:
        if "403" in str(e) or "insufficient" in str(e).lower():
            print(f"   ⚠️  No permission for rules endpoint")
        else:
            print(f"   ❌ Error: {str(e)[:100]}")
    
    print("\n" + "=" * 60)
    if successful_tests > 0:
        print(f"✅ Connection test completed!")
        print(f"   Authentication: Working")
        print(f"   API Access: {successful_tests}/{total_tests} endpoints accessible")
        print("=" * 60)
        
        if successful_tests < total_tests:
            print("\n⚠️  Some endpoints require additional permissions.")
            print("   To grant more permissions:")
            print("   1. Log into QRadar Console")
            print("   2. Go to Admin → Authorized Services")
            print("   3. Edit your service and add required permissions:")
            print("      - Ariel (for event queries)")
            print("      - Offenses (for offense data)")
            print("      - Assets (for asset information)")
            print("      - Log Sources (for log source management)")
            print("      - Rules (for analytics rules)")
            print("      - System (for system information)")
        
        print("\n✅ You can now configure this server with Claude Desktop.")
        print("   See SETUP.md for instructions.")
    else:
        print(f"⚠️  Authentication works but no API endpoints are accessible!")
        print("=" * 60)
        print("\n❌ Your API token needs permissions. Please:")
        print("   1. Log into QRadar Console")
        print("   2. Go to Admin → Authorized Services")
        print("   3. Edit or recreate your service with required permissions")
        print("   4. Update your .env file with the new token")
        sys.exit(1)
    print()


if __name__ == "__main__":
    test_connection()

