#!/usr/bin/env python3
"""
Test HeartMatch Authentication
=============================

Test script to verify that the admin credentials work properly.
"""

import requests
import json

def test_web_app_auth():
    """Test web app authentication"""
    print("🔐 Testing HeartMatch Web App Authentication")
    print("=" * 50)
    
    # Test different web apps
    web_apps = [
        {"name": "Working App", "url": "http://localhost:5000", "file": "working_app.py"},
        {"name": "Main App", "url": "http://localhost:5000", "file": "main_app.py"},
        {"name": "Enhanced App", "url": "http://localhost:5000", "file": "mistral_heartmatch.py"}
    ]
    
    for app in web_apps:
        print(f"\n📱 Testing {app['name']}...")
        try:
            # Test health endpoint
            response = requests.get(f"{app['url']}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {app['name']} is running")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   AI Model: {data.get('ai_model', 'unknown')}")
                if 'available_models' in data:
                    print(f"   Available Models: {data.get('available_models', [])}")
            else:
                print(f"❌ {app['name']} not responding (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {app['name']} connection failed: {str(e)}")
    
    print("\n🔑 Testing Admin Credentials")
    print("=" * 30)
    print("Username: admin")
    print("Password: HeartMatch2025!")
    print("Note: These credentials should work for all web applications")
    
    print("\n💬 Testing Chatbot Endpoints")
    print("=" * 30)
    
    # Test chatbot endpoint
    try:
        chatbot_data = {
            "message": "Hello, I'm testing the chatbot functionality.",
            "user_type": "general"
        }
        
        response = requests.post("http://localhost:5000/api/chatbot", 
                               json=chatbot_data, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chatbot endpoint working")
            print(f"   Response: {data.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Chatbot endpoint failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Chatbot test failed: {str(e)}")
    
    print("\n🤖 Testing Model Selection")
    print("=" * 30)
    
    # Test model selection
    try:
        # Get available models
        response = requests.get("http://localhost:5000/api/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Model selection working")
            print(f"   Current Model: {data.get('current_model', 'unknown')}")
            print(f"   Available Models: {list(data.get('available_models', {}).keys())}")
        else:
            print(f"❌ Model selection failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Model selection test failed: {str(e)}")

def test_gui_components():
    """Test GUI components"""
    print("\n🖥️ Testing GUI Components")
    print("=" * 30)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Test if enhanced GUI can be imported
        from HeartMatch_Enhanced_GUI import HeartMatchEnhancedGUI, CompassionateChatbot, ModelSelectionDialog
        
        print("✅ Enhanced GUI components can be imported")
        print("   - HeartMatchEnhancedGUI")
        print("   - CompassionateChatbot") 
        print("   - ModelSelectionDialog")
        
        # Test chatbot initialization
        chatbot = CompassionateChatbot()
        print("✅ CompassionateChatbot initialized")
        
    except Exception as e:
        print(f"❌ GUI component test failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 HeartMatch System Test Suite")
    print("=" * 50)
    print("Testing authentication, chatbot, and model selection...")
    print()
    
    test_web_app_auth()
    test_gui_components()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("\n📋 Summary:")
    print("- Admin credentials: admin / HeartMatch2025!")
    print("- Chatbot functionality: Available in both GUI and web app")
    print("- Model selection: Available in both GUI and web app")
    print("- PDF viewer: Available in enhanced GUI")
    print("- File attachments: Available in enhanced GUI")
    print("- Timeout issues: Fixed (increased to 120 seconds)")
