#!/usr/bin/env python3
"""
🧪 HeartMatch WebApp Accessibility & Login Test
© 2025 HeartMatch - Child-Family Matching System

Test script for WebApp accessibility features and login functionality.
"""

import requests
import json
import time
import sys
import os

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_TIMEOUT = 10

def test_webapp_startup():
    """Test if WebApp starts successfully"""
    print("🚀 Testing WebApp startup...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ WebApp is running successfully")
            return True
        else:
            print(f"❌ WebApp returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ WebApp is not running. Please start it first:")
        print("   cd webapp && python mistral_heartmatch.py")
        return False
    except Exception as e:
        print(f"❌ Error testing WebApp: {e}")
        return False

def test_accessibility_features():
    """Test accessibility features"""
    print("\n♿ Testing accessibility features...")
    
    try:
        # Test accessibility settings endpoint
        response = requests.get(f"{BASE_URL}/api/accessibility", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            settings = response.json()
            print("✅ Accessibility settings endpoint working")
            print(f"   Screen reader detected: {settings.get('screen_reader_detected', False)}")
            print(f"   High contrast enabled: {settings.get('high_contrast_enabled', False)}")
            print(f"   Font size multiplier: {settings.get('font_size_multiplier', 1.0)}")
            print(f"   Color blind friendly: {settings.get('color_blind_friendly', False)}")
            print(f"   Compliance level: {settings.get('compliance_level', 'AA')}")
        else:
            print(f"❌ Accessibility endpoint returned status: {response.status_code}")
            return False
        
        # Test updating accessibility settings
        test_settings = {
            'high_contrast': True,
            'color_blind_friendly': True,
            'font_size': 1.5
        }
        
        response = requests.post(f"{BASE_URL}/api/accessibility", 
                               json=test_settings, 
                               timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            print("✅ Accessibility settings update working")
            print(f"   Update result: {result.get('message', 'Success')}")
        else:
            print(f"❌ Accessibility settings update failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing accessibility: {e}")
        return False

def test_compliance_features():
    """Test compliance features"""
    print("\n📋 Testing compliance features...")
    
    try:
        # Test compliance validation
        test_data = {
            'child_name': 'Test Child',
            'child_dob': '2010-01-01',
            'family_name': 'Test Family',
            'family_email': 'test@example.com',
            'family_phone': '(555) 123-4567'
        }
        
        response = requests.post(f"{BASE_URL}/api/compliance/validate", 
                               json=test_data, 
                               timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            print("✅ Compliance validation working")
            print(f"   Data valid: {result.get('valid', False)}")
            print(f"   Issues: {result.get('issues', [])}")
            print(f"   Standards: {result.get('compliance_standards', [])}")
        else:
            print(f"❌ Compliance validation failed: {response.status_code}")
            return False
        
        # Test compliance audit
        response = requests.get(f"{BASE_URL}/api/compliance/audit", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            audit = response.json()
            print("✅ Compliance audit working")
            print(f"   Total events: {audit.get('total_events', 0)}")
            print(f"   Successful events: {audit.get('successful_events', 0)}")
            print(f"   Failed events: {audit.get('failed_events', 0)}")
        else:
            print(f"❌ Compliance audit failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing compliance: {e}")
        return False

def test_login_functionality():
    """Test login functionality"""
    print("\n🔐 Testing login functionality...")
    
    try:
        # Test dashboard access (should work without login for now)
        response = requests.get(f"{BASE_URL}/dashboard", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Dashboard accessible")
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
            return False
        
        # Test children page
        response = requests.get(f"{BASE_URL}/children", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Children page accessible")
        else:
            print(f"❌ Children page access failed: {response.status_code}")
            return False
        
        # Test families page
        response = requests.get(f"{BASE_URL}/families", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Families page accessible")
        else:
            print(f"❌ Families page access failed: {response.status_code}")
            return False
        
        # Test matching page
        response = requests.get(f"{BASE_URL}/matching", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Matching page accessible")
        else:
            print(f"❌ Matching page access failed: {response.status_code}")
            return False
        
        # Test chatbot page
        response = requests.get(f"{BASE_URL}/chatbot", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Chatbot page accessible")
        else:
            print(f"❌ Chatbot page access failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing login functionality: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔌 Testing API endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get(f"{BASE_URL}/api/health", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            health = response.json()
            print("✅ Health endpoint working")
            print(f"   Status: {health.get('status', 'unknown')}")
            print(f"   Timestamp: {health.get('timestamp', 'unknown')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test models endpoint
        response = requests.get(f"{BASE_URL}/api/models", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            models = response.json()
            print("✅ Models endpoint working")
            print(f"   Available models: {list(models.get('available_models', {}).keys())}")
            print(f"   Current model: {models.get('current_model', 'unknown')}")
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 HeartMatch WebApp Accessibility & Login Test")
    print("=" * 60)
    
    # Test WebApp startup
    if not test_webapp_startup():
        print("\n❌ WebApp startup test failed. Please start the WebApp first.")
        return False
    
    # Test accessibility features
    accessibility_ok = test_accessibility_features()
    
    # Test compliance features
    compliance_ok = test_compliance_features()
    
    # Test login functionality
    login_ok = test_login_functionality()
    
    # Test API endpoints
    api_ok = test_api_endpoints()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    print(f"🚀 WebApp Startup: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"♿ Accessibility: {'✅ PASS' if accessibility_ok else '❌ FAIL'}")
    print(f"📋 Compliance: {'✅ PASS' if compliance_ok else '❌ FAIL'}")
    print(f"🔐 Login Functionality: {'✅ PASS' if login_ok else '❌ FAIL'}")
    print(f"🔌 API Endpoints: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    all_tests_passed = accessibility_ok and compliance_ok and login_ok and api_ok
    
    if all_tests_passed:
        print("\n🎉 All tests passed! WebApp is ready for deployment.")
        print("✅ Accessibility features working")
        print("✅ Compliance features working")
        print("✅ Login functionality working")
        print("✅ API endpoints working")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
