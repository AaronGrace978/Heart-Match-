#!/usr/bin/env python3
"""
📥 HeartMatch Model Downloader
© 2025 HeartMatch - Child-Family Matching System

Downloads required AI models for local deployment.
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path

# Add models directory to path
sys.path.append(str(Path(__file__).parent / "models"))
from model_manager import ModelManager

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    print("🔍 Checking Ollama installation...")
    
    # Check if ollama command exists
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ Ollama not installed")
        print("📋 Please install Ollama first:")
        print("   1. Visit: https://ollama.ai/download")
        print("   2. Download and install Ollama")
        print("   3. Start Ollama service")
        print("   4. Run this script again")
        return False
    
    # Check if Ollama service is running
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
        else:
            print("❌ Ollama service not responding")
            return False
    except Exception as e:
        print(f"❌ Ollama service not accessible: {e}")
        print("📋 Please start Ollama service:")
        print("   - Windows: Run 'ollama serve' in command prompt")
        print("   - Or start Ollama from Start Menu")
        return False

def download_models():
    """Download all required models"""
    print("\n🚀 Starting model download process...")
    
    manager = ModelManager()
    
    # Check Ollama installation
    if not check_ollama_installation():
        return False
    
    # Setup required models
    success = manager.setup_required_models()
    
    if success:
        print("\n🎉 All required models downloaded successfully!")
        
        # Show model information
        print("\n📊 Installed Models:")
        installed_models = manager.get_installed_models()
        for model in installed_models:
            print(f"   ✅ {model}")
        
        # Create model configuration
        manager.create_model_config()
        
        return True
    else:
        print("\n❌ Model download incomplete")
        print("📋 Some models may have failed to download")
        return False

def show_model_sizes():
    """Show estimated model sizes"""
    print("\n📏 Model Size Information:")
    print("   mistral:7b     - ~4.1GB")
    print("   qwen2.5:7b     - ~4.4GB") 
    print("   llama2:7b      - ~3.8GB")
    print("   Total required - ~12.3GB")
    print("\n💡 Make sure you have enough disk space!")

def main():
    """Main download function"""
    print("📥 HeartMatch Model Downloader")
    print("=" * 50)
    
    # Show model sizes
    show_model_sizes()
    
    # Ask for confirmation
    print("\n⚠️  This will download ~12GB of AI models")
    response = input("Continue? (y/N): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("❌ Download cancelled")
        return
    
    # Download models
    if download_models():
        print("\n✅ Model download complete!")
        print("🚀 HeartMatch is ready to use")
        print("\n📋 Next steps:")
        print("1. Run HeartMatch GUI: python HeartMatch_Enhanced_GUI.py")
        print("2. Test WebApp: cd webapp && python mistral_heartmatch.py")
        print("3. Deploy to Sundai.club when ready")
    else:
        print("\n❌ Model download failed")
        print("📋 Please check your internet connection and try again")

if __name__ == "__main__":
    main()
