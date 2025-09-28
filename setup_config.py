#!/usr/bin/env python3
"""
🔧 HeartMatch Configuration Setup
© 2025 HeartMatch - Child-Family Matching System

Setup script for configuring API keys for Sundai.club deployment.
"""

import os
import json
import sys

def setup_config():
    """Setup configuration for HeartMatch deployment"""
    print("🔧 HeartMatch Configuration Setup")
    print("=" * 50)
    
    # Check if config.json already exists
    if os.path.exists('config.json'):
        print("✅ config.json already exists")
        return
    
    # Check if template exists
    if not os.path.exists('config_template.json'):
        print("❌ config_template.json not found")
        return
    
    print("📋 Setting up configuration...")
    
    # Copy template to config.json
    try:
        with open('config_template.json', 'r') as f:
            template = json.load(f)
        
        # Update with placeholder API key
        template['ollama_cloud']['api_key'] = 'YOUR_OLLAMA_CLOUD_API_KEY_HERE'
        
        with open('config.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        print("✅ config.json created successfully")
        print("🔑 Please update the API key in config.json")
        print("📝 Replace 'YOUR_OLLAMA_CLOUD_API_KEY_HERE' with your actual API key")
        
    except Exception as e:
        print(f"❌ Error creating config.json: {e}")

def check_config():
    """Check if configuration is properly set up"""
    print("\n🔍 Checking configuration...")
    
    if not os.path.exists('config.json'):
        print("❌ config.json not found")
        return False
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        api_key = config.get('ollama_cloud', {}).get('api_key', '')
        
        if api_key == 'YOUR_OLLAMA_CLOUD_API_KEY_HERE':
            print("⚠️  API key not configured - using placeholder")
            return False
        elif api_key:
            print("✅ API key configured")
            return True
        else:
            print("❌ No API key found in configuration")
            return False
            
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 HeartMatch Configuration Setup")
    print("=" * 50)
    
    # Setup configuration
    setup_config()
    
    # Check configuration
    is_configured = check_config()
    
    if is_configured:
        print("\n🎉 Configuration setup complete!")
        print("✅ HeartMatch is ready for deployment")
    else:
        print("\n⚠️  Configuration setup incomplete")
        print("📝 Please update config.json with your API key")
        print("🔑 Get your API key from: https://ollama.ai/cloud")
    
    print("\n📋 Next steps:")
    print("1. Update config.json with your API key")
    print("2. Test the configuration")
    print("3. Deploy to Sundai.club")

if __name__ == "__main__":
    main()
