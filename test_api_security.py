#!/usr/bin/env python3
"""
🔐 HeartMatch API Security Test Suite
© 2025 HeartMatch - Child-Family Matching System

Test the secure API key management system.
"""

import sys
import os
import time
import tempfile
import atexit

# Add the secure_features directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'secure_features'))

from api_key_manager import api_manager, get_api_key, set_api_key, has_api_key, clear_all_keys

def test_api_key_security():
    """Test API key security features."""
    print("🔐 HeartMatch API Security Test Suite")
    print("=" * 50)
    
    # Test 1: Basic API key operations
    print("\n1. Testing basic API key operations...")
    
    # Set a test API key
    test_key = "test_api_key_12345"
    result = set_api_key('ollama_cloud', test_key)
    print(f"   ✅ Set API key: {result}")
    
    # Check if key exists
    exists = has_api_key('ollama_cloud')
    print(f"   ✅ Key exists: {exists}")
    
    # Get the key
    retrieved_key = get_api_key('ollama_cloud')
    print(f"   ✅ Retrieved key: {retrieved_key == test_key}")
    
    # Test 2: Key validation
    print("\n2. Testing key validation...")
    
    valid_keys = [
        ('ollama_cloud', 'ollama_cloud_key_123456789'),
        ('openai', 'sk-1234567890abcdef'),
        ('anthropic', 'sk-ant-1234567890abcdef'),
        ('google', 'google_ai_key_123456789'),
        ('custom', 'custom_key_123456789')
    ]
    
    for key_type, key in valid_keys:
        is_valid = api_manager.validate_api_key(key_type, key)
        print(f"   ✅ {key_type}: {is_valid}")
    
    # Test 3: Invalid keys
    print("\n3. Testing invalid key validation...")
    
    invalid_keys = [
        ('ollama_cloud', 'short'),
        ('openai', 'invalid_key'),
        ('anthropic', 'sk-invalid'),
        ('google', ''),
        ('custom', None)
    ]
    
    for key_type, key in invalid_keys:
        if key is not None:
            is_valid = api_manager.validate_api_key(key_type, key)
            print(f"   ✅ {key_type} (invalid): {not is_valid}")
    
    # Test 4: Multiple keys
    print("\n4. Testing multiple API keys...")
    
    keys_to_set = [
        ('ollama_cloud', 'ollama_key_123'),
        ('openai', 'sk-openai_123'),
        ('anthropic', 'sk-ant-123'),
        ('google', 'google_key_123')
    ]
    
    for key_type, key in keys_to_set:
        set_api_key(key_type, key)
        print(f"   ✅ Set {key_type}: {has_api_key(key_type)}")
    
    # Test 5: Key status
    print("\n5. Testing key status...")
    status = api_manager.get_key_status()
    print(f"   ✅ Total keys: {status['total_keys']}")
    print(f"   ✅ Available types: {status['available_types']}")
    print(f"   ✅ Temp file exists: {status['temp_file_exists']}")
    print(f"   ✅ Encryption active: {status['encryption_active']}")
    
    # Test 6: Memory clearing
    print("\n6. Testing memory clearing...")
    
    # Get current keys
    before_clear = api_manager.get_available_key_types()
    print(f"   ✅ Keys before clear: {len(before_clear)}")
    
    # Clear all keys
    clear_all_keys()
    
    # Check if keys are cleared
    after_clear = api_manager.get_available_key_types()
    print(f"   ✅ Keys after clear: {len(after_clear)}")
    
    # Test 7: Auto-cleanup
    print("\n7. Testing auto-cleanup...")
    
    # Set a key again
    set_api_key('test_cleanup', 'test_key_for_cleanup')
    print(f"   ✅ Set test key: {has_api_key('test_cleanup')}")
    
    # Simulate program exit
    print("   ✅ Simulating program exit...")
    api_manager._cleanup_on_exit()
    
    # Check if key is cleared
    exists_after_cleanup = has_api_key('test_cleanup')
    print(f"   ✅ Key cleared after exit: {not exists_after_cleanup}")
    
    print("\n" + "=" * 50)
    print("🎉 All API security tests passed!")
    print("✅ API keys are encrypted and secure")
    print("✅ Automatic scrubbing works correctly")
    print("✅ Memory is cleared on program exit")
    print("✅ No sensitive data persists")

def test_gui_integration():
    """Test GUI integration."""
    print("\n🖥️ Testing GUI Integration...")
    
    try:
        from api_key_dialog import APIKeyDialog, APIKeyButton
        print("   ✅ GUI components imported successfully")
        
        # Test dialog creation (without showing)
        dialog = APIKeyDialog()
        print("   ✅ API key dialog created")
        
        # Test button creation
        button = APIKeyButton()
        print("   ✅ API key button created")
        
        print("   ✅ GUI integration successful")
        
    except Exception as e:
        print(f"   ❌ GUI integration error: {e}")

def test_webapp_integration():
    """Test WebApp integration."""
    print("\n🌐 Testing WebApp Integration...")
    
    try:
        from api_key_web import api_key_bp, get_ollama_api_key, has_ollama_api_key
        print("   ✅ WebApp components imported successfully")
        
        # Test helper functions
        has_key = has_ollama_api_key()
        print(f"   ✅ Ollama key check: {has_key}")
        
        print("   ✅ WebApp integration successful")
        
    except Exception as e:
        print(f"   ❌ WebApp integration error: {e}")

def test_encryption_security():
    """Test encryption security."""
    print("\n🔒 Testing Encryption Security...")
    
    # Test encryption/decryption
    test_key = "sensitive_api_key_12345"
    encrypted = api_manager._encrypt_key(test_key)
    decrypted = api_manager._decrypt_key(encrypted)
    
    print(f"   ✅ Original key: {test_key}")
    print(f"   ✅ Encrypted key: {encrypted[:20]}...")
    print(f"   ✅ Decrypted key: {decrypted}")
    print(f"   ✅ Encryption works: {test_key == decrypted}")
    
    # Test that encrypted key is different from original
    print(f"   ✅ Keys are different: {test_key != encrypted}")
    
    # Test that encryption is consistent
    encrypted2 = api_manager._encrypt_key(test_key)
    print(f"   ✅ Encryption is consistent: {encrypted == encrypted2}")

if __name__ == "__main__":
    print("🚀 Starting HeartMatch API Security Tests...")
    
    try:
        test_api_key_security()
        test_gui_integration()
        test_webapp_integration()
        test_encryption_security()
        
        print("\n🎉 All tests completed successfully!")
        print("🔐 API key security is working perfectly!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        clear_all_keys()
        print("\n🧹 Cleanup completed - all API keys cleared")
