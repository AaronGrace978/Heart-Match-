#!/usr/bin/env python3
"""
🧪 HeartMatch GUI Test Fix
© 2025 HeartMatch - Child-Family Matching System

Quick test to verify GUI launches without accessibility features.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    
    print("✅ PyQt5 imports successful")
    
    # Test basic GUI creation
    app = QApplication(sys.argv)
    print("✅ QApplication created successfully")
    
    # Test if we can import the main GUI class
    try:
        from HeartMatch_Enhanced_GUI import HeartMatchEnhancedGUI
        print("✅ HeartMatchEnhancedGUI class imported successfully")
        
        # Test GUI creation
        window = HeartMatchEnhancedGUI()
        print("✅ HeartMatchEnhancedGUI instance created successfully")
        
        print("\n🎉 GUI test successful! The application should launch properly.")
        print("📋 Status: All imports and class creation working")
        
    except Exception as e:
        print(f"❌ Error creating GUI: {e}")
        print("🔧 This indicates there's still an issue with the GUI code")
        
except ImportError as e:
    print(f"❌ PyQt5 import failed: {e}")
    print("📋 Please install PyQt5: pip install PyQt5")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n" + "="*50)
print("🧪 GUI Test Complete")
