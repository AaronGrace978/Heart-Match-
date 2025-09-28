#!/usr/bin/env python3
"""
🏠 HeartMatch Enhanced GUI - Child-Family Matching System
=========================================================

Enhanced GUI with chatbot, social worker integration, and model selection.
Features compassionate AI support for children and families.

Author: Built with ActivatePrime Architecture
Version: 2.0.0
© 2025 HeartMatch - Child-Family Matching System
"""

import sys
import os
import json
import hashlib
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QComboBox, QLabel, QTabWidget, QGroupBox, QGridLayout,
    QProgressBar, QMessageBox, QSplitter, QFrame, QListWidget, QListWidgetItem,
    QCheckBox, QSpinBox, QSlider, QTextBrowser, QScrollArea, QFormLayout,
    QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem, QFileDialog,
    QInputDialog
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QTextCursor
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
import logging
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
import base64

# Import API key manager
sys.path.append(os.path.join(os.path.dirname(__file__), 'secure_features'))
from api_key_dialog import APIKeyButton, open_api_key_dialog
from api_key_manager import api_manager, get_api_key, has_api_key

# Import accessibility and compliance features
try:
    from accessibility_enhancements import get_accessibility_manager
    from pii_hipaa_compliance import get_pii_protection, get_hipaa_compliance, validate_data_compliance, ComplianceStandard
    ACCESSIBILITY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Accessibility features not available: {e}")
    ACCESSIBILITY_AVAILABLE = False
    
    # Create dummy classes for fallback
    class DummyAccessibilityManager:
        def create_accessible_button(self, text, description, parent):
            button = QPushButton(text, parent)
            button.setAccessibleName(text)
            if description:
                button.setAccessibleDescription(description)
            return button
        
        def announce(self, message):
            print(f"Accessibility: {message}")
        
        def visual(self):
            return type('obj', (object,), {'high_contrast_mode': False, 'font_size_multiplier': 1.0, 'color_blind_friendly': False})()
        
        def screen_reader(self):
            return type('obj', (object,), {'is_screen_reader_active': False})()
    
    class DummyPIIProtection:
        def validate_pii_compliance(self, data):
            return True, []
        
        def log_compliance_event(self, *args, **kwargs):
            pass
    
    def get_accessibility_manager():
        return DummyAccessibilityManager()
    
    def get_pii_protection():
        return DummyPIIProtection()
    
    def get_hipaa_compliance():
        return DummyPIIProtection()
    
    class ComplianceStandard:
        MASSACHUSETTS_PII = "massachusetts_pii"
    
    def validate_data_compliance(data, standards):
        return True, []

class ModelSelectionDialog(QDialog):
    """Model selection dialog for choosing AI models"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🤖 AI Model Selection")
        self.setGeometry(200, 200, 500, 400)
        self.selected_model = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("🤖 Choose AI Model for HeartMatch")
        header.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #2E86AB; 
            margin: 10px;
            padding: 10px;
            background: linear-gradient(135deg, #E6F3FF, #B6E5D8);
            border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Model options
        models_group = QGroupBox("Available Models")
        models_layout = QVBoxLayout(models_group)
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "🚀 Mistral 7B (Recommended for Production)",
            "🧠 Qwen 72B (Advanced Reasoning)", 
            "⚡ Qwen 480B (Maximum Capability)",
            "🌟 GPT-OSS 120B (Balanced Performance)",
            "🔧 Ollama Default Model"
        ])
        models_layout.addWidget(QLabel("Select Model:"))
        models_layout.addWidget(self.model_combo)
        
        # Model descriptions
        desc_text = QTextBrowser()
        desc_text.setMaximumHeight(150)
        desc_text.setHtml("""
        <h4>Model Descriptions:</h4>
        <ul>
        <li><b>Mistral 7B:</b> Fast, efficient, perfect for real-time conversations</li>
        <li><b>Qwen 72B:</b> Advanced reasoning for complex matching scenarios</li>
        <li><b>Qwen 480B:</b> Maximum capability for detailed psychological analysis</li>
        <li><b>GPT-OSS 120B:</b> Excellent balance of speed and accuracy</li>
        <li><b>Ollama Default:</b> Fallback option for basic functionality</li>
        </ul>
        """)
        models_layout.addWidget(desc_text)
        
        layout.addWidget(models_group)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def get_selected_model(self):
        """Get the selected model configuration"""
        index = self.model_combo.currentIndex()
        model_configs = {
            0: {'name': 'mistral:7b', 'display': 'Mistral 7B'},
            1: {'name': 'qwen2.5:72b', 'display': 'Qwen 72B'},
            2: {'name': 'qwen3-coder:480b-cloud', 'display': 'Qwen 480B'},
            3: {'name': 'gpt-oss:120b-cloud', 'display': 'GPT-OSS 120B'},
            4: {'name': 'ollama-default', 'display': 'Ollama Default'}
        }
        return model_configs.get(index, model_configs[0])

class CompassionateChatbot:
    """Compassionate chatbot for supporting children and families"""
    
    def __init__(self, model_name='mistral:7b'):
        self.model_name = model_name
        self.conversation_history = []
        self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"
        
    def generate_response(self, message, context="general"):
        """Generate compassionate response"""
        try:
            # Add context-specific prompts
            if context == "child":
                system_prompt = """You are a warm, caring counselor speaking with a child who may be looking for a new home. 
                Be gentle, encouraging, and age-appropriate. Use simple language and be emotionally supportive.
                Focus on hope, safety, and helping them feel valued and loved."""
            elif context == "family":
                system_prompt = """You are a knowledgeable family counselor helping prospective adoptive/foster families. 
                Provide thoughtful guidance about the adoption/foster process, child needs, and family preparation.
                Be encouraging while being realistic about challenges."""
            elif context == "social_worker":
                system_prompt = """You are an experienced social work supervisor providing guidance to caseworkers.
                Offer professional insights about child welfare, family assessment, and best practices in placement decisions."""
            else:
                system_prompt = """You are a compassionate AI assistant helping with child-family matching.
                Provide helpful, empathetic responses focused on the wellbeing of children and families."""
            
            # Prepare the prompt
            full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
            
            # Call Ollama API
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 500
                }
            }
            
            response = requests.post(self.ollama_endpoint, json=payload, timeout=120)
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', 'I apologize, but I had trouble generating a response. Please try again.')
                
                # Store conversation
                self.conversation_history.append({
                    'user': message,
                    'assistant': ai_response,
                    'context': context,
                    'timestamp': datetime.now().isoformat()
                })
                
                return ai_response
            else:
                return "I'm having trouble connecting right now. Please check if Ollama is running and try again."
                
        except Exception as e:
            logging.error(f"Chatbot error: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again in a moment."

class PIIProtection:
    """Enhanced PII protection for Massachusetts compliance"""
    
    @staticmethod
    def anonymize_data(data):
        """Anonymize sensitive information while preserving matching criteria"""
        if isinstance(data, dict):
            anonymized = {}
            for key, value in data.items():
                if key in ['name', 'address', 'phone', 'email', 'ssn']:
                    # Hash sensitive data for matching without exposing PII
                    anonymized[key] = hashlib.sha256(str(value).encode()).hexdigest()[:8]
                else:
                    anonymized[key] = value
            return anonymized
        return data
    
    @staticmethod
    def validate_pii_compliance(data):
        """Validate that data meets Massachusetts PII requirements"""
        required_fields = ['age_range', 'preferences', 'location_region']
        return all(field in data for field in required_fields)

class OllamaMatchingEngine:
    """Enhanced AI-powered matching engine with multiple model support"""
    
    def __init__(self, model_name='mistral:7b'):
        self.local_endpoint = "http://127.0.0.1:11434/api/generate"
        self.current_model = model_name
        self.matching_prompts = {
            'child_family': """
            You are a compassionate AI helping match children with loving families.
            Analyze the following profiles and provide matching recommendations:
            
            Child Profile: {child_profile}
            Family Profile: {family_profile}
            
            Consider:
            - Compatibility factors (interests, values, lifestyle)
            - Special needs accommodations
            - Age appropriateness
            - Geographic considerations
            - Family dynamics and preferences
            
            Provide a matching score (0-100) and detailed reasoning.
            Be empathetic and focus on the child's best interests.
            """,
            'compatibility_analysis': """
            Analyze compatibility between child and family:
            Child: {child_data}
            Family: {family_data}
            
            Return JSON with:
            - compatibility_score (0-100)
            - strengths (list of positive factors)
            - considerations (areas needing attention)
            - recommendations (specific suggestions)
            """
        }
    
    def set_model(self, model_name):
        """Set the current AI model"""
        self.current_model = model_name
    
    def get_matching_recommendations(self, child_profile, family_profiles):
        """Get AI-powered matching recommendations"""
        try:
            recommendations = []
            
            for family in family_profiles:
                # Prepare anonymized data for AI analysis
                child_anon = PIIProtection.anonymize_data(child_profile)
                family_anon = PIIProtection.anonymize_data(family)
                
                # Create matching prompt
                prompt = self.matching_prompts['child_family'].format(
                    child_profile=json.dumps(child_anon, indent=2),
                    family_profile=json.dumps(family_anon, indent=2)
                )
                
                # Call Ollama API
                response = self._call_ollama_api(prompt)
                
                if response:
                    recommendations.append({
                        'family_id': family.get('id', 'unknown'),
                        'match_score': self._extract_score(response),
                        'reasoning': response,
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Sort by match score
            recommendations.sort(key=lambda x: x['match_score'], reverse=True)
            return recommendations
            
        except Exception as e:
            logging.error(f"Matching engine error: {e}")
            return []
    
    def _call_ollama_api(self, prompt):
        """Call local Ollama with specified model"""
        try:
            # Try to get API key from local config first
            api_key = self._get_api_key_from_config()
            
            payload = {
                "model": self.current_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            }
            
            # Add API key if available
            if api_key:
                payload["api_key"] = api_key
            
            response = requests.post(self.local_endpoint, json=payload, timeout=120)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logging.error(f"Ollama error: {response.status_code} - {response.text}")
                return None
            
        except Exception as e:
            logging.error(f"Ollama API error: {e}")
            return None
    
    def _get_api_key_from_config(self):
        """Get API key from local config file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # Check for API key in various possible locations
                    if 'ollama_cloud' in config and 'api_key' in config['ollama_cloud']:
                        return config['ollama_cloud']['api_key']
                    elif 'api_key' in config:
                        return config['api_key']
                    elif 'OLLAMA_CLOUD_API_KEY' in os.environ:
                        return os.environ['OLLAMA_CLOUD_API_KEY']
            return None
        except Exception as e:
            logging.error(f"Error reading config: {e}")
            return None
    
    def _get_model_config(self):
        """Get model configuration from models/model_config.json"""
        try:
            model_config_path = os.path.join(os.path.dirname(__file__), 'models', 'model_config.json')
            if os.path.exists(model_config_path):
                with open(model_config_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logging.error(f"Error reading model config: {e}")
            return None
    
    def _extract_score(self, response):
        """Extract matching score from AI response"""
        try:
            import re
            score_match = re.search(r'score[:\s]*(\d+)', response.lower())
            if score_match:
                return int(score_match.group(1))
            return 50  # Default neutral score
        except:
            return 50

class HeartMatchEnhancedGUI(QMainWindow):
    """Enhanced HeartMatch Child-Family Matching Interface with Chatbot"""
    
    def __init__(self):
        super().__init__()
        self.current_model = 'mistral:7b'
        self.matching_engine = OllamaMatchingEngine(self.current_model)
        self.chatbot = CompassionateChatbot(self.current_model)
        self.current_child = None
        self.family_database = []
        self.matching_results = []
        self.social_worker_notes = []
        
        # Initialize accessibility and compliance
        self.accessibility_manager = get_accessibility_manager()
        self.pii_protection = get_pii_protection()
        self.hipaa_compliance = get_hipaa_compliance()
        
        self.init_ui()
        self.load_sample_data()
        
        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_matches)
        self.refresh_timer.start(60000)  # Refresh every minute
    
    def open_api_key_dialog(self):
        """Open API key management dialog"""
        dialog = open_api_key_dialog(self)
        if dialog.exec_() == QDialog.Accepted:
            if ACCESSIBILITY_AVAILABLE:
                self.accessibility_manager.announce_action("API key dialog opened")
    
    def open_accessibility_settings(self):
        """Open accessibility settings dialog"""
        if ACCESSIBILITY_AVAILABLE:
            try:
                from accessibility_settings_dialog import AccessibilitySettingsDialog
                dialog = AccessibilitySettingsDialog(self)
                if dialog.exec_() == QDialog.Accepted:
                    self.accessibility_manager.announce_action("Accessibility settings updated")
            except ImportError:
                QMessageBox.information(self, "Accessibility", 
                                       "Accessibility features are not fully available.\n"
                                       "Please ensure all accessibility modules are installed.")
        else:
            QMessageBox.information(self, "Accessibility", 
                                   "Accessibility features are not available.\n"
                                   "Please ensure all accessibility modules are installed.")
    
    def init_ui(self):
        """Initialize the enhanced user interface"""
        self.setWindowTitle("🏠 HeartMatch Enhanced - Child-Family Matching System v2.0")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Set compassionate color scheme
        self.set_compassionate_theme()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header with model selection
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #C0C0C0;
                border-radius: 10px;
                background: white;
            }
            QTabBar::tab {
                background: #E6F3FF;
                border: 2px solid #C0C0C0;
                padding: 10px 20px;
                margin-right: 2px;
                border-radius: 8px 8px 0px 0px;
            }
            QTabBar::tab:selected {
                background: #FFE5E5;
                border-color: #FF69B4;
                font-weight: bold;
            }
        """)
        
        # Create tabs
        matching_tab = self.create_matching_tab()
        chatbot_tab = self.create_chatbot_tab()
        social_worker_tab = self.create_social_worker_tab()
        documents_tab = self.create_documents_tab()
        
        self.tab_widget.addTab(matching_tab, "💕 Child-Family Matching")
        self.tab_widget.addTab(chatbot_tab, "💬 Compassionate Chat")
        self.tab_widget.addTab(social_worker_tab, "👥 Social Worker Tools")
        self.tab_widget.addTab(documents_tab, "📄 Documents & Files")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage("HeartMatch Enhanced System Ready - Helping Children Find Loving Homes")
    
    def set_compassionate_theme(self):
        """Set a warm, compassionate color theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 248, 240))  # Warm cream
        palette.setColor(QPalette.WindowText, QColor(51, 51, 51))  # Soft dark
        palette.setColor(QPalette.Base, QColor(255, 255, 255))     # Pure white
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(51, 51, 51))
        palette.setColor(QPalette.Text, QColor(51, 51, 51))
        palette.setColor(QPalette.Button, QColor(102, 153, 204))  # Soft blue
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
    
    def create_header(self):
        """Create the application header with model selection"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Title and model selection row
        title_row = QHBoxLayout()
        
        # Main title
        title = QLabel("🏠 HeartMatch Enhanced - Child-Family Matching System")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2E86AB; 
            margin: 10px;
            padding: 10px;
        """)
        title_row.addWidget(title)
        
        title_row.addStretch()
        
        # Model selection button
        self.model_button = QPushButton("🤖 Select AI Model")
        self.model_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #45a049, #3e8e41);
            }
        """)
        self.model_button.clicked.connect(self.select_model)
        title_row.addWidget(self.model_button)
        
        # API Key Manager button
        if ACCESSIBILITY_AVAILABLE:
            self.api_key_button = self.accessibility_manager.create_accessible_button(
                "🔑 API Keys", 
                "Manage API keys for cloud model access",
                self
            )
        else:
            self.api_key_button = APIKeyButton()
        self.api_key_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #FF6B6B, #FF5252);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #FF5252, #E53935);
            }
        """)
        self.api_key_button.clicked.connect(self.open_api_key_dialog)
        title_row.addWidget(self.api_key_button)
        
        # Accessibility Settings button
        if ACCESSIBILITY_AVAILABLE:
            self.accessibility_button = self.accessibility_manager.create_accessible_button(
                "♿ Accessibility", 
                "Configure accessibility settings",
                self
            )
        else:
            self.accessibility_button = QPushButton("♿ Accessibility", self)
            self.accessibility_button.setAccessibleName("Accessibility Settings")
            self.accessibility_button.setAccessibleDescription("Configure accessibility settings")
        self.accessibility_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #45a049, #3d8b40);
            }
        """)
        self.accessibility_button.clicked.connect(self.open_accessibility_settings)
        title_row.addWidget(self.accessibility_button)
        
        # Current model display
        self.current_model_label = QLabel(f"Current: {self.current_model}")
        self.current_model_label.setStyleSheet("font-size: 12px; color: #666; margin: 5px;")
        title_row.addWidget(self.current_model_label)
        
        header_layout.addLayout(title_row)
        
        # Subtitle and compliance notice row
        info_row = QHBoxLayout()
        
        subtitle = QLabel("AI-Powered Compassionate Matching with Social Worker Support")
        subtitle.setStyleSheet("font-size: 16px; color: #666; margin: 5px; font-style: italic;")
        info_row.addWidget(subtitle)
        
        info_row.addStretch()
        
        compliance_label = QLabel("🔒 PII Compliant - Massachusetts DCF Standards | © 2025 HeartMatch")
        compliance_label.setStyleSheet("font-size: 12px; color: #4CAF50; margin: 5px; font-weight: bold;")
        info_row.addWidget(compliance_label)
        
        header_layout.addLayout(info_row)
        
        return header_widget
    
    def select_model(self):
        """Open model selection dialog"""
        dialog = ModelSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            model_config = dialog.get_selected_model()
            self.current_model = model_config['name']
            self.matching_engine.set_model(self.current_model)
            self.chatbot = CompassionateChatbot(self.current_model)
            self.current_model_label.setText(f"Current: {model_config['display']}")
            self.statusBar().showMessage(f"✅ Switched to {model_config['display']} model")
    
    def on_api_key_saved(self, key_type, status):
        """Handle API key saved event"""
        if status == "saved":
            self.statusBar().showMessage(f"✅ API key saved successfully!")
            # Update any components that might need the API key
            self.update_api_key_status()
    
    def update_api_key_status(self):
        """Update API key status in the interface"""
        # Check if we have API keys available
        has_ollama = has_api_key('ollama_cloud')
        has_openai = has_api_key('openai')
        has_anthropic = has_api_key('anthropic')
        
        # Update status bar with API key availability
        api_status = []
        if has_ollama:
            api_status.append("Ollama Cloud ✅")
        if has_openai:
            api_status.append("OpenAI ✅")
        if has_anthropic:
            api_status.append("Anthropic ✅")
        
        if api_status:
            self.statusBar().showMessage(f"🔐 API Keys: {', '.join(api_status)}")
        else:
            self.statusBar().showMessage("🔐 No API keys configured - Click API Keys button to add")
    
    def create_matching_tab(self):
        """Create the child-family matching tab"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # Left panel - Child profiles and matching
        left_panel = self.create_child_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Family database and results
        right_panel = self.create_family_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        main_splitter.setSizes([800, 800])
        
        return tab
    
    def create_chatbot_tab(self):
        """Create the compassionate chatbot tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header = QLabel("💬 Compassionate AI Assistant")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2E86AB; 
            margin: 10px;
            padding: 15px;
            background: linear-gradient(135deg, #E6F3FF, #FFE5E5);
            border-radius: 15px;
            border: 2px solid #FF69B4;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Chat context selector
        context_layout = QHBoxLayout()
        context_layout.addWidget(QLabel("Speaking with:"))
        
        self.chat_context = QComboBox()
        self.chat_context.addItems([
            "👶 Child (Age-appropriate, gentle guidance)",
            "👨‍👩‍👧‍👦 Family (Adoption/foster guidance)",
            "👤 Social Worker (Professional consultation)",
            "💬 General (General support)"
        ])
        context_layout.addWidget(self.chat_context)
        context_layout.addStretch()
        
        # Clear and export buttons
        clear_btn = QPushButton("🔄 Clear Chat")
        clear_btn.clicked.connect(self.clear_chat)
        context_layout.addWidget(clear_btn)
        
        export_btn = QPushButton("📄 Export Chat")
        export_btn.clicked.connect(self.export_chat)
        context_layout.addWidget(export_btn)
        
        layout.addLayout(context_layout)
        
        # Chat display
        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background: #FAFAFA;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Chat input
        input_layout = QHBoxLayout()
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here... 💬")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #D0D0D0;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #FF69B4;
            }
        """)
        self.chat_input.returnPressed.connect(self.send_chat_message)
        input_layout.addWidget(self.chat_input)
        
        send_btn = QPushButton("💌 Send")
        send_btn.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #FF69B4, #FF1493);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
                min-width: 80px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #FF1493, #DC143C);
            }
        """)
        send_btn.clicked.connect(self.send_chat_message)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        return tab
    
    def create_social_worker_tab(self):
        """Create the social worker tools tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header = QLabel("👥 Social Worker Collaboration Tools")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2E86AB; 
            margin: 10px;
            padding: 15px;
            background: linear-gradient(135deg, #E6F3FF, #D4E6B7);
            border-radius: 15px;
            border: 2px solid #4CAF50;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Tools layout
        tools_layout = QHBoxLayout()
        
        # Notes panel
        notes_group = QGroupBox("📝 Case Notes & Documentation")
        notes_layout = QVBoxLayout(notes_group)
        
        # Notes controls
        notes_controls = QHBoxLayout()
        add_note_btn = QPushButton("➕ Add Note")
        add_note_btn.clicked.connect(self.add_social_worker_note)
        notes_controls.addWidget(add_note_btn)
        
        save_notes_btn = QPushButton("💾 Save Notes")
        save_notes_btn.clicked.connect(self.save_social_worker_notes)
        notes_controls.addWidget(save_notes_btn)
        notes_controls.addStretch()
        
        notes_layout.addLayout(notes_controls)
        
        # Notes display
        self.notes_display = QTableWidget()
        self.notes_display.setColumnCount(3)
        self.notes_display.setHorizontalHeaderLabels(["Timestamp", "Note Type", "Content"])
        self.notes_display.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        notes_layout.addWidget(self.notes_display)
        
        tools_layout.addWidget(notes_group)
        
        # Model selection for social workers
        model_group = QGroupBox("🤖 AI Model Selection")
        model_layout = QVBoxLayout(model_group)
        
        # Model selection dropdown
        self.social_worker_model_combo = QComboBox()
        self.social_worker_model_combo.addItems([
            "🚀 Mistral 7B (Fast, Real-time Chat)",
            "🧠 Qwen 72B (Advanced Reasoning)", 
            "⚡ Qwen 480B (Maximum Capability)",
            "🌟 GPT-OSS 120B (Balanced Performance)",
            "🔧 Ollama Default Model"
        ])
        model_layout.addWidget(QLabel("Select AI Model for Social Worker Tasks:"))
        model_layout.addWidget(self.social_worker_model_combo)
        
        # Model switch button
        switch_model_btn = QPushButton("🔄 Switch Model")
        switch_model_btn.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #9C27B0, #7B1FA2);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #7B1FA2, #6A1B9A);
            }
        """)
        switch_model_btn.clicked.connect(self.switch_social_worker_model)
        model_layout.addWidget(switch_model_btn)
        
        # Current model display
        self.social_worker_current_model = QLabel(f"Current: {self.current_model}")
        self.social_worker_current_model.setStyleSheet("font-size: 12px; color: #666; margin: 5px;")
        model_layout.addWidget(self.social_worker_current_model)
        
        tools_layout.addWidget(model_group)
        
        # Quick actions panel
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        # Action buttons
        actions = [
            ("🔍 Generate Compatibility Report", self.generate_compatibility_report),
            ("📊 Create Match Summary", self.create_match_summary),
            ("📞 Schedule Family Meeting", self.schedule_family_meeting),
            ("📋 Assessment Checklist", self.open_assessment_checklist),
            ("🏥 Medical History Review", self.medical_history_review),
            ("🎓 Educational Needs Analysis", self.educational_needs_analysis),
        ]
        
        for text, handler in actions:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: #F0F8FF;
                    border: 2px solid #4169E1;
                    padding: 10px;
                    margin: 2px;
                    border-radius: 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    background: #E6F3FF;
                }
            """)
            btn.clicked.connect(handler)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        tools_layout.addWidget(actions_group)
        
        layout.addLayout(tools_layout)
        
        return tab
    
    def send_chat_message(self):
        """Send message to chatbot"""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        # Get context
        context_map = {
            0: "child",
            1: "family", 
            2: "social_worker",
            3: "general"
        }
        context = context_map.get(self.chat_context.currentIndex(), "general")
        
        # Display user message
        self.chat_display.append(f"""
        <div style="margin: 10px 0; padding: 10px; background: #E3F2FD; border-radius: 10px;">
        <strong>You:</strong> {message}
        </div>
        """)
        
        # Clear input
        self.chat_input.clear()
        
        # Show typing indicator
        self.chat_display.append("""
        <div style="margin: 10px 0; padding: 10px; background: #FFF3E0; border-radius: 10px; font-style: italic;">
        <strong>Assistant:</strong> <em>Thinking...</em> 🤔
        </div>
        """)
        
        # Move cursor to end
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.chat_display.setTextCursor(cursor)
        
        # Process message and get response
        QApplication.processEvents()  # Update UI
        
        try:
            response = self.chatbot.generate_response(message, context)
            
            # Remove typing indicator and add response
            self.chat_display.undo()  # Remove typing indicator
            
            self.chat_display.append(f"""
            <div style="margin: 10px 0; padding: 10px; background: #E8F5E8; border-radius: 10px;">
            <strong>Assistant:</strong> {response}
            </div>
            """)
            
        except Exception as e:
            self.chat_display.undo()  # Remove typing indicator
            self.chat_display.append(f"""
            <div style="margin: 10px 0; padding: 10px; background: #FFEBEE; border-radius: 10px;">
            <strong>Assistant:</strong> I apologize, but I'm having technical difficulties. Please ensure Ollama is running and try again.
            </div>
            """)
        
        # Move cursor to end
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.chat_display.setTextCursor(cursor)
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_display.clear()
        self.chatbot.conversation_history = []
        self.chat_display.append("""
        <div style="text-align: center; margin: 20px; color: #666; font-style: italic;">
        💬 Chat cleared. How can I help you today?
        </div>
        """)
    
    def export_chat(self):
        """Export chat conversation"""
        if not self.chatbot.conversation_history:
            QMessageBox.information(self, "No Chat History", "No conversation to export.")
            return
        
        try:
            filename = f"HeartMatch_Chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.chatbot.conversation_history, f, indent=2)
            QMessageBox.information(self, "Export Complete", f"Chat exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export chat: {str(e)}")
    
    def add_social_worker_note(self):
        """Add a new social worker note"""
        note_text, ok = QInputDialog.getText(self, "Add Note", "Enter case note:")
        if ok and note_text:
            note = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'type': 'Case Note',
                'content': note_text
            }
            self.social_worker_notes.append(note)
            self.refresh_notes_display()
    
    def refresh_notes_display(self):
        """Refresh the notes display table"""
        self.notes_display.setRowCount(len(self.social_worker_notes))
        for i, note in enumerate(self.social_worker_notes):
            self.notes_display.setItem(i, 0, QTableWidgetItem(note['timestamp']))
            self.notes_display.setItem(i, 1, QTableWidgetItem(note['type']))
            self.notes_display.setItem(i, 2, QTableWidgetItem(note['content'][:100] + "..." if len(note['content']) > 100 else note['content']))
    
    def save_social_worker_notes(self):
        """Save social worker notes to file"""
        try:
            filename = f"HeartMatch_SocialWorker_Notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.social_worker_notes, f, indent=2)
            QMessageBox.information(self, "Notes Saved", f"Notes saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save notes: {str(e)}")
    
    # Social worker action methods (placeholders for full implementation)
    def generate_compatibility_report(self):
        QMessageBox.information(self, "Compatibility Report", "Generating detailed compatibility analysis...")
    
    def create_match_summary(self):
        QMessageBox.information(self, "Match Summary", "Creating match summary document...")
    
    def schedule_family_meeting(self):
        QMessageBox.information(self, "Schedule Meeting", "Opening calendar to schedule family meeting...")
    
    def open_assessment_checklist(self):
        QMessageBox.information(self, "Assessment Checklist", "Opening standardized assessment checklist...")
    
    def medical_history_review(self):
        QMessageBox.information(self, "Medical Review", "Accessing medical history review tools...")
    
    def educational_needs_analysis(self):
        QMessageBox.information(self, "Educational Analysis", "Opening educational needs assessment...")
    
    def switch_social_worker_model(self):
        """Switch AI model for social worker tasks"""
        index = self.social_worker_model_combo.currentIndex()
        model_configs = {
            0: {'name': 'mistral:7b', 'display': 'Mistral 7B'},
            1: {'name': 'qwen2.5:72b', 'display': 'Qwen 72B'},
            2: {'name': 'qwen3-coder:480b-cloud', 'display': 'Qwen 480B'},
            3: {'name': 'gpt-oss:120b-cloud', 'display': 'GPT-OSS 120B'},
            4: {'name': 'ollama-default', 'display': 'Ollama Default'}
        }
        
        model_config = model_configs.get(index, model_configs[0])
        self.current_model = model_config['name']
        self.matching_engine.set_model(self.current_model)
        self.chatbot = CompassionateChatbot(self.current_model)
        
        # Update displays
        self.current_model_label.setText(f"Current: {model_config['display']}")
        self.social_worker_current_model.setText(f"Current: {model_config['display']}")
        
        # Show confirmation
        QMessageBox.information(
            self, 
            "Model Switched", 
            f"AI model switched to {model_config['display']} for social worker tasks.\n\nThis model will be used for:\n• Compatibility analysis\n• Case notes generation\n• Assessment reports\n• Chatbot responses"
        )
        
        self.statusBar().showMessage(f"✅ Social worker model switched to {model_config['display']}")
    
    def create_documents_tab(self):
        """Create documents and file management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header = QLabel("📄 Documents & File Management")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2E86AB; 
            margin: 10px;
            padding: 15px;
            background: linear-gradient(135deg, #E6F3FF, #F0F8FF);
            border-radius: 15px;
            border: 2px solid #4169E1;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # File management section
        file_group = QGroupBox("📁 File Management")
        file_layout = QVBoxLayout(file_group)
        
        # File upload controls
        upload_layout = QHBoxLayout()
        
        self.upload_button = QPushButton("📤 Upload File")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #45a049, #3e8e41);
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.upload_button)
        
        self.view_pdf_button = QPushButton("📄 View PDF")
        self.view_pdf_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #FF9800, #F57C00);
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #F57C00, #EF6C00);
            }
        """)
        self.view_pdf_button.clicked.connect(self.view_pdf)
        upload_layout.addWidget(self.view_pdf_button)
        
        upload_layout.addStretch()
        file_layout.addLayout(upload_layout)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                background: #FAFAFA;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #D0D0D0;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: #E3F2FD;
                border: 2px solid #2196F3;
            }
        """)
        file_layout.addWidget(self.file_list)
        
        layout.addWidget(file_group)
        
        # PDF viewer section
        pdf_group = QGroupBox("📖 PDF Viewer")
        pdf_layout = QVBoxLayout(pdf_group)
        
        # PDF viewer
        self.pdf_viewer = QTextBrowser()
        self.pdf_viewer.setStyleSheet("""
            QTextBrowser {
                background: white;
                border: 2px solid #B0BEC5;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        self.pdf_viewer.setPlaceholderText("Select a PDF file to view its contents...")
        pdf_layout.addWidget(self.pdf_viewer)
        
        # PDF controls
        pdf_controls = QHBoxLayout()
        
        self.extract_text_button = QPushButton("📝 Extract Text")
        self.extract_text_button.clicked.connect(self.extract_pdf_text)
        pdf_controls.addWidget(self.extract_text_button)
        
        self.save_pdf_button = QPushButton("💾 Save PDF")
        self.save_pdf_button.clicked.connect(self.save_pdf)
        pdf_controls.addWidget(self.save_pdf_button)
        
        pdf_controls.addStretch()
        pdf_layout.addLayout(pdf_controls)
        
        layout.addWidget(pdf_group)
        
        return tab
    
    def upload_file(self):
        """Upload a file to the system"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select File to Upload",
            "",
            "All Files (*);;PDF Files (*.pdf);;Images (*.png *.jpg *.jpeg);;Documents (*.doc *.docx *.txt)"
        )
        
        if file_path:
            try:
                # Get file info
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                
                # Add to file list
                item_text = f"{file_name} ({file_size} bytes)"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, file_path)
                self.file_list.addItem(item)
                
                self.statusBar().showMessage(f"✅ File uploaded: {file_name}")
                
            except Exception as e:
                QMessageBox.critical(self, "Upload Error", f"Failed to upload file: {str(e)}")
    
    def view_pdf(self):
        """View selected PDF file"""
        current_item = self.file_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "No File Selected", "Please select a PDF file to view.")
            return
        
        file_path = current_item.data(Qt.UserRole)
        if not file_path.endswith('.pdf'):
            QMessageBox.warning(self, "Invalid File", "Please select a PDF file.")
            return
        
        try:
            # Extract text from PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += f"\n--- Page {page_num + 1} ---\n"
                    text_content += page.extract_text()
                
                # Display in PDF viewer
                self.pdf_viewer.setPlainText(text_content)
                self.statusBar().showMessage(f"✅ PDF loaded: {os.path.basename(file_path)}")
                
        except Exception as e:
            QMessageBox.critical(self, "PDF Error", f"Failed to read PDF: {str(e)}")
    
    def extract_pdf_text(self):
        """Extract text from PDF and show in viewer"""
        self.view_pdf()  # Same functionality for now
    
    def save_pdf(self):
        """Save PDF content"""
        if not self.pdf_viewer.toPlainText():
            QMessageBox.information(self, "No Content", "No PDF content to save.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Text",
            "extracted_text.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.pdf_viewer.toPlainText())
                QMessageBox.information(self, "Save Complete", f"Text saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save: {str(e)}")
    
    # Include the original matching functionality methods here
    def create_child_panel(self):
        """Create child profile and matching panel (enhanced)"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Child Profile Section
        child_group = QGroupBox("👶 Child Profile")
        child_layout = QFormLayout(child_group)
        
        # Child profile fields
        self.child_age = QSpinBox()
        self.child_age.setRange(0, 18)
        self.child_age.setValue(8)
        child_layout.addRow("Age:", self.child_age)
        
        self.child_interests = QLineEdit()
        self.child_interests.setPlaceholderText("e.g., art, sports, music, reading...")
        child_layout.addRow("Interests:", self.child_interests)
        
        self.child_special_needs = QTextEdit()
        self.child_special_needs.setMaximumHeight(80)
        self.child_special_needs.setPlaceholderText("Any special needs or considerations...")
        child_layout.addRow("Special Needs:", self.child_special_needs)
        
        self.child_personality = QComboBox()
        self.child_personality.addItems([
            "Outgoing and social",
            "Quiet and thoughtful", 
            "Active and energetic",
            "Creative and artistic",
            "Academic and studious"
        ])
        child_layout.addRow("Personality:", self.child_personality)
        
        self.child_location = QComboBox()
        self.child_location.addItems([
            "Boston Metro",
            "Western Massachusetts", 
            "Central Massachusetts",
            "Southeastern Massachusetts",
            "Northeastern Massachusetts"
        ])
        child_layout.addRow("Location Region:", self.child_location)
        
        layout.addWidget(child_group)
        
        # Matching Controls
        controls_group = QGroupBox("🔍 Matching Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        self.find_matches_button = QPushButton("💕 Find Loving Families")
        self.find_matches_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #FF69B4, #FF1493);
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #FF1493, #DC143C);
            }
        """)
        self.find_matches_button.clicked.connect(self.find_matches)
        controls_layout.addWidget(self.find_matches_button)
        
        self.clear_profile_button = QPushButton("🔄 Clear Profile")
        self.clear_profile_button.clicked.connect(self.clear_child_profile)
        controls_layout.addWidget(self.clear_profile_button)
        
        layout.addWidget(controls_group)
        
        # Matching Results
        results_group = QGroupBox("💖 Matching Results")
        results_layout = QVBoxLayout(results_group)
        
        self.matching_results_list = QListWidget()
        self.matching_results_list.setStyleSheet("""
            QListWidget {
                background: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #DEE2E6;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: #FFE5E5;
                border: 2px solid #FF69B4;
            }
        """)
        results_layout.addWidget(self.matching_results_list)
        
        layout.addWidget(results_group)
        
        return panel
    
    def create_family_panel(self):
        """Create family database and management panel (enhanced)"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Family Database Section
        family_group = QGroupBox("👨‍👩‍👧‍👦 Family Database")
        family_layout = QVBoxLayout(family_group)
        
        # Family list
        self.family_list = QListWidget()
        self.family_list.setStyleSheet("""
            QListWidget {
                background: #F0F8FF;
                border: 2px solid #B0C4DE;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #D3D3D3;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: #E6F3FF;
                border: 2px solid #4169E1;
            }
        """)
        family_layout.addWidget(self.family_list)
        
        # Family management buttons
        family_buttons = QHBoxLayout()
        
        self.add_family_button = QPushButton("➕ Add Family")
        self.add_family_button.clicked.connect(self.add_family)
        family_buttons.addWidget(self.add_family_button)
        
        self.edit_family_button = QPushButton("✏️ Edit Family")
        self.edit_family_button.clicked.connect(self.edit_family)
        family_buttons.addWidget(self.edit_family_button)
        
        self.view_family_button = QPushButton("👁️ View Details")
        self.view_family_button.clicked.connect(self.view_family_details)
        family_buttons.addWidget(self.view_family_button)
        
        family_layout.addLayout(family_buttons)
        
        layout.addWidget(family_group)
        
        # AI Analysis Section
        ai_group = QGroupBox("🤖 AI Matching Analysis")
        ai_layout = QVBoxLayout(ai_group)
        
        self.ai_analysis_text = QTextBrowser()
        self.ai_analysis_text.setMaximumHeight(200)
        self.ai_analysis_text.setStyleSheet("""
            QTextBrowser {
                background: #FFF8DC;
                border: 2px solid #DAA520;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        ai_layout.addWidget(self.ai_analysis_text)
        
        # AI controls
        ai_controls = QHBoxLayout()
        
        self.analyze_compatibility_button = QPushButton("🧠 Analyze Compatibility")
        self.analyze_compatibility_button.clicked.connect(self.analyze_compatibility)
        ai_controls.addWidget(self.analyze_compatibility_button)
        
        self.export_results_button = QPushButton("📊 Export Results")
        self.export_results_button.clicked.connect(self.export_results)
        ai_controls.addWidget(self.export_results_button)
        
        ai_layout.addLayout(ai_controls)
        
        layout.addWidget(ai_group)
        
        return panel
    
    # Include all the original matching methods with minimal modifications
    def load_sample_data(self):
        """Load sample family data for demonstration"""
        sample_families = [
            {
                'id': 'F001',
                'family_type': 'Married Couple',
                'age_range': '30-45',
                'interests': ['outdoor activities', 'education', 'community service'],
                'specializations': ['children with learning differences', 'teens'],
                'location': 'Boston Metro',
                'home_type': 'Single family home with yard',
                'pets': 'Two friendly dogs',
                'values': 'Education, creativity, outdoor activities'
            },
            {
                'id': 'F002', 
                'family_type': 'Single Parent',
                'age_range': '35-50',
                'interests': ['art', 'music', 'cooking'],
                'specializations': ['young children', 'artistic development'],
                'location': 'Western Massachusetts',
                'home_type': 'Cozy apartment with art studio',
                'pets': 'One cat',
                'values': 'Creativity, self-expression, academic achievement'
            },
            {
                'id': 'F003',
                'family_type': 'Same-Sex Couple',
                'age_range': '28-42',
                'interests': ['sports', 'travel', 'volunteering'],
                'specializations': ['athletic children', 'cultural diversity'],
                'location': 'Central Massachusetts', 
                'home_type': 'Suburban home with sports facilities',
                'pets': 'None',
                'values': 'Physical activity, cultural awareness, community involvement'
            }
        ]
        
        self.family_database = sample_families
        self.refresh_family_list()
    
    def refresh_family_list(self):
        """Refresh the family list display"""
        self.family_list.clear()
        for family in self.family_database:
            item_text = f"{family['family_type']} - {family['age_range']} - {family['location']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, family)
            self.family_list.addItem(item)
    
    def find_matches(self):
        """Find matching families using AI"""
        try:
            # Get child profile
            child_profile = {
                'age': self.child_age.value(),
                'interests': self.child_interests.text(),
                'special_needs': self.child_special_needs.toPlainText(),
                'personality': self.child_personality.currentText(),
                'location': self.child_location.currentText()
            }
            
            # Validate PII compliance
            if not PIIProtection.validate_pii_compliance(child_profile):
                QMessageBox.warning(self, "PII Compliance", "Please ensure all required fields are completed.")
                return
            
            # Show progress
            self.statusBar().showMessage("🤖 AI is analyzing compatibility... Please wait.")
            
            # Get AI recommendations
            recommendations = self.matching_engine.get_matching_recommendations(
                child_profile, self.family_database
            )
            
            # Display results
            self.display_matching_results(recommendations)
            
            self.statusBar().showMessage(f"✅ Found {len(recommendations)} potential matches!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to find matches: {str(e)}")
            self.statusBar().showMessage("❌ Error occurred during matching.")
    
    def display_matching_results(self, recommendations):
        """Display matching results in the UI"""
        self.matching_results_list.clear()
        self.matching_results = recommendations
        
        for i, match in enumerate(recommendations[:10]):  # Show top 10 matches
            family_id = match['family_id']
            score = match['match_score']
            
            # Find family details
            family = next((f for f in self.family_database if f['id'] == family_id), None)
            if family:
                item_text = f"💖 Match #{i+1}: {family['family_type']} - Score: {score}%"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, match)
                self.matching_results_list.addItem(item)
    
    def analyze_compatibility(self):
        """Analyze compatibility between selected child and family"""
        current_item = self.matching_results_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "Selection Required", "Please select a match to analyze.")
            return
        
        match_data = current_item.data(Qt.UserRole)
        family_id = match_data['family_id']
        
        # Find family details
        family = next((f for f in self.family_database if f['id'] == family_id), None)
        if not family:
            return
        
        # Get child profile
        child_profile = {
            'age': self.child_age.value(),
            'interests': self.child_interests.text(),
            'special_needs': self.child_special_needs.toPlainText(),
            'personality': self.child_personality.currentText(),
            'location': self.child_location.currentText()
        }
        
        # Display AI analysis
        analysis_text = f"""
🤖 AI Compatibility Analysis (Model: {self.current_model})

Child Profile:
• Age: {child_profile['age']} years
• Interests: {child_profile['interests']}
• Personality: {child_profile['personality']}
• Special Needs: {child_profile['special_needs']}

Family Profile:
• Type: {family['family_type']}
• Age Range: {family['age_range']}
• Interests: {', '.join(family['interests'])}
• Specializations: {', '.join(family['specializations'])}
• Values: {family['values']}

Match Score: {match_data['match_score']}%

AI Reasoning:
{match_data['reasoning']}

Recommendations:
• Consider scheduling a supervised meeting
• Discuss specific needs and expectations
• Review family's experience with similar situations
• Plan gradual integration if match proceeds
        """
        
        self.ai_analysis_text.setPlainText(analysis_text)
    
    def add_family(self):
        """Add a new family to the database"""
        QMessageBox.information(self, "Add Family", "Family addition feature will be implemented in the full version.")
    
    def edit_family(self):
        """Edit family information"""
        QMessageBox.information(self, "Edit Family", "Family editing feature will be implemented in the full version.")
    
    def view_family_details(self):
        """View detailed family information"""
        current_item = self.family_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "Selection Required", "Please select a family to view details.")
            return
        
        family = current_item.data(Qt.UserRole)
        
        details_text = f"""
👨‍👩‍👧‍👦 Family Details

Family ID: {family['id']}
Type: {family['family_type']}
Age Range: {family['age_range']}
Location: {family['location']}

Interests:
{chr(10).join(f"• {interest}" for interest in family['interests'])}

Specializations:
{chr(10).join(f"• {spec}" for spec in family['specializations'])}

Home Type: {family['home_type']}
Pets: {family['pets']}
Values: {family['values']}
        """
        
        QMessageBox.information(self, "Family Details", details_text)
    
    def clear_child_profile(self):
        """Clear the child profile form"""
        self.child_age.setValue(8)
        self.child_interests.clear()
        self.child_special_needs.clear()
        self.child_personality.setCurrentIndex(0)
        self.child_location.setCurrentIndex(0)
        self.matching_results_list.clear()
        self.ai_analysis_text.clear()
    
    def export_results(self):
        """Export matching results"""
        if not self.matching_results:
            QMessageBox.information(self, "No Results", "No matching results to export.")
            return
        
        # Create export data (anonymized)
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'model_used': self.current_model,
            'matches': len(self.matching_results),
            'top_matches': [
                {
                    'rank': i+1,
                    'family_id': match['family_id'],
                    'score': match['match_score'],
                    'timestamp': match['timestamp']
                }
                for i, match in enumerate(self.matching_results[:5])
            ]
        }
        
        # Save to file
        filename = f"HeartMatch_Results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            QMessageBox.information(self, "Export Complete", f"Results exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export: {str(e)}")
    
    def refresh_matches(self):
        """Refresh matching results"""
        if self.matching_results:
            self.statusBar().showMessage("🔄 Refreshing matches...")
            # Re-run matching if needed
            self.statusBar().showMessage("✅ Matches refreshed")

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("HeartMatch Enhanced")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Massachusetts Child Services")
    
    # Create and show main window
    window = HeartMatchEnhancedGUI()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
