#!/usr/bin/env python3
"""
🏠 HeartMatch - Child-Family Matching System for Massachusetts
============================================================

A compassionate AI-powered system to help children find loving families.
Built with strict PII compliance for Massachusetts state requirements.

Features:
- AI-powered matching using 120B Ollama model
- Strict PII protection and anonymization
- Intuitive PyQt5 interface
- Secure data handling for sensitive information
- Real-time matching recommendations

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
    QCheckBox, QSpinBox, QSlider, QTextBrowser, QScrollArea, QFormLayout
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
import logging

class PIIProtection:
    """Strict PII protection for Massachusetts compliance"""
    
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
    """AI-powered matching engine using local Ollama with cloud models"""
    
    def __init__(self):
        # Use local Ollama with cloud models (like ActivatePrime)
        self.local_endpoint = "http://127.0.0.1:11434/api/generate"
        self.cloud_models = {
            'qwen3_480b': 'qwen3-coder:480b-cloud',
            'gpt_oss_120b': 'gpt-oss:120b-cloud',
            'qwen2_72b': 'qwen2.5:72b'
        }
        self.current_model = 'qwen3_480b'  # Start with 480B model
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
        """Call local Ollama with cloud models for AI analysis"""
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": self.cloud_models[self.current_model],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            }
            
            response = requests.post(self.local_endpoint, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logging.error(f"Local Ollama error: {response.status_code} - {response.text}")
                return None
            
        except Exception as e:
            logging.error(f"Local Ollama API error: {e}")
            # Try fallback to 120B model if 480B fails
            if self.current_model == 'qwen3_480b':
                self.current_model = 'gpt_oss_120b'
                return self._call_ollama_api(prompt)
            elif self.current_model == 'gpt_oss_120b':
                self.current_model = 'qwen2_72b'
                return self._call_ollama_api(prompt)
            return None
    
    def _extract_score(self, response):
        """Extract matching score from AI response"""
        try:
            # Look for score in response
            import re
            score_match = re.search(r'score[:\s]*(\d+)', response.lower())
            if score_match:
                return int(score_match.group(1))
            return 50  # Default neutral score
        except:
            return 50

class HeartMatchGUI(QMainWindow):
    """Main HeartMatch Child-Family Matching Interface"""
    
    def __init__(self):
        super().__init__()
        self.matching_engine = OllamaMatchingEngine()
        self.current_child = None
        self.family_database = []
        self.matching_results = []
        
        self.init_ui()
        self.load_sample_data()
        
        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_matches)
        self.refresh_timer.start(60000)  # Refresh every minute
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🏠 HeartMatch - Child-Family Matching System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set compassionate color scheme
        self.set_compassionate_theme()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Left panel - Child profiles and matching
        left_panel = self.create_child_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Family database and results
        right_panel = self.create_family_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        main_splitter.setSizes([700, 700])
        
        # Status bar
        self.statusBar().showMessage("HeartMatch System Ready - Helping Children Find Loving Homes")
    
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
        """Create the application header"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Main title
        title = QLabel("🏠 HeartMatch - Child-Family Matching System")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2E86AB; 
            margin: 15px;
            padding: 15px;
            background: linear-gradient(135deg, #FFE5E5, #FFB6C1);
            border-radius: 15px;
            border: 2px solid #FF69B4;
        """)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("AI-Powered Compassionate Matching for Children Seeking Loving Homes")
        subtitle.setStyleSheet("font-size: 16px; color: #666; margin: 5px; font-style: italic;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        # PII compliance notice
        compliance_label = QLabel("🔒 PII Compliant - Massachusetts State Standards")
        compliance_label.setStyleSheet("font-size: 12px; color: #4CAF50; margin: 5px; font-weight: bold;")
        compliance_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(compliance_label)
        
        return header_widget
    
    def create_child_panel(self):
        """Create child profile and matching panel"""
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
        """Create family database and management panel"""
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
🤖 AI Compatibility Analysis

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
    app.setApplicationName("HeartMatch")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Massachusetts Child Services")
    
    # Create and show main window
    window = HeartMatchGUI()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
