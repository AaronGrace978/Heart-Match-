# 🏠 HeartMatch Enhanced - Child-Family Matching System v2.0

A compassionate AI-powered system designed to help children find loving families in Massachusetts. Built with strict PII compliance and using advanced AI models for intelligent matching.

**© 2025 HeartMatch - Child-Family Matching System**

## 💙 Mission Statement

HeartMatch is dedicated to creating meaningful connections between children seeking homes and loving families. Our AI-powered system ensures that every match is carefully analyzed for compatibility, special needs, and long-term success.

## ✨ Key Features

### 🤖 AI-Powered Matching
- **Multiple AI Models**: Mistral 7B, Qwen 72B, Qwen 480B, GPT-OSS 120B
- **Model Selection**: Choose the best model for your needs
- **Intelligent Scoring**: Provides detailed compatibility scores (0-100%)
- **Comprehensive Analysis**: Considers interests, special needs, personality, and values
- **Ollama Cloud Integration**: Access to larger models via local Ollama

### 🔒 PII Compliance
- **Massachusetts State Standards**: Full compliance with state PII regulations
- **Data Anonymization**: Sensitive information is protected while preserving matching criteria
- **Secure Processing**: All data handling follows strict privacy protocols

### 🎨 Enhanced User Interface
- **Intuitive PyQt5 GUI**: Clean, compassionate design with tabs
- **💬 Compassionate Chatbot**: Age-appropriate support for children and families
- **👥 Social Worker Tools**: Case notes, compatibility reports, assessment tools
- **🤖 Model Selection**: Choose between different AI models
- **Real-time Matching**: Instant AI-powered recommendations
- **Detailed Analysis**: Comprehensive compatibility reports
- **Export Capabilities**: Save and share matching results

## 🔑 API Key Configuration

**⚠️ IMPORTANT: Ollama Cloud API Key Required**

The HeartMatch system requires an Ollama Cloud subscription to access larger AI models (480B, 120B). Here's where to configure your API key:

### 1. Get Your Ollama Cloud API Key
- Visit: https://ollama.ai/cloud
- Sign up for Ollama Cloud subscription
- Copy your API key from the dashboard

### 2. Configure API Key in HeartMatch
The API key is configured in the following files:

**For GUI Applications:**
- File: `D:\DCF Project\HeartMatch_Enhanced_GUI.py`
- Line: `self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"`
- Note: Uses local Ollama with cloud model access

**For Web Applications:**
- File: `D:\DCF Project\webapp\mistral_heartmatch.py`
- Line: `self.ollama_endpoint = "http://127.0.0.1:11434/api/generate"`
- Note: Local Ollama service with cloud model integration

**For ActivatePrime Integration:**
- File: `D:\ActivatePrime\config\ollama_cloud_config.json`
- Contains your Ollama Cloud API key
- HeartMatch automatically uses this configuration

### 3. Model Access
With Ollama Cloud subscription, you get access to:
- **Mistral 7B** (recommended for real-time chat)
- **Qwen 72B** (advanced reasoning)
- **Qwen 480B** (maximum capability)
- **GPT-OSS 120B** (balanced performance)

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8+ 
- **Ollama Cloud Subscription Required** (for access to larger models)
- **API Key Required** (see configuration section below)
- 8GB+ RAM (for local models), 16GB+ recommended for cloud models

### Installation

1. **Clone or download** this repository
2. **Configure API Key** (see API Key Configuration below)
3. **Run the launcher**:
   ```
   Launch_HeartMatch.bat          # Original GUI
   Launch_Enhanced_GUI.bat        # Enhanced GUI with chatbot
   ```
4. **Follow the setup wizard** - the system will:
   - Check Python installation
   - Start Ollama service
   - Download AI models (Mistral 7B, Qwen 72B, etc.)
   - Install required packages
   - Launch HeartMatch

### Manual Installation

If you prefer manual setup:

```bash
# Install Python packages
pip install -r requirements.txt

# Start Ollama service
ollama serve

# Download 120B model
ollama pull qwen2.5:120b

# Launch HeartMatch
python HeartMatch_Child_Family_Matching_System.py
```

## 🎯 How It Works

### 1. Child Profile Creation
- Enter child's age, interests, and special needs
- Specify personality traits and location preferences
- All data is anonymized for PII compliance

### 2. AI-Powered Matching
- The 120B model analyzes compatibility factors
- Considers special needs accommodations
- Evaluates family dynamics and preferences
- Provides detailed reasoning for each match

### 3. Comprehensive Results
- View top 10 matching families
- Get detailed compatibility analysis
- Export results for case workers
- Track matching history

## 🏛️ Massachusetts Compliance

### PII Protection
- **Data Anonymization**: Personal identifiers are hashed
- **Secure Storage**: No sensitive data stored in plain text
- **Audit Trail**: Complete logging of all matching activities
- **Access Controls**: Role-based permissions for different user types

### State Standards
- **HIPAA Compliant**: Healthcare information protection
- **FERPA Compliant**: Educational records protection
- **State Privacy Laws**: Full Massachusetts compliance
- **Regular Audits**: Built-in compliance monitoring

## 🔧 Technical Architecture

### AI Engine
- **Ollama Integration**: Local 120B model for privacy
- **Custom Prompts**: Specialized for child-family matching
- **Real-time Analysis**: Instant compatibility scoring
- **Fallback Models**: Automatic model switching if needed

### Data Security
- **Encryption**: All data encrypted at rest and in transit
- **Access Logging**: Complete audit trail
- **Backup Systems**: Automated data protection
- **Recovery Procedures**: Disaster recovery protocols

## 📊 Sample Data

The system includes sample family profiles for demonstration:
- **Family F001**: Married couple, Boston Metro, education-focused
- **Family F002**: Single parent, Western MA, arts-oriented  
- **Family F003**: Same-sex couple, Central MA, sports-focused

## 🛠️ Customization

### Adding New Families
- Use the "Add Family" button in the interface
- Complete family profile forms
- Specify specializations and preferences
- Set location and availability

### Modifying AI Prompts
- Edit matching prompts in the `OllamaMatchingEngine` class
- Customize compatibility criteria
- Adjust scoring algorithms
- Add new analysis factors

## 🌐 Web Application

The HeartMatch system also includes a full web application:

### Web App Features
- **🌐 Browser-based Interface**: Access from any device
- **💬 Compassionate Chatbot**: Web-based AI support
- **👥 Social Worker Dashboard**: Case management tools
- **📊 Real-time Analytics**: Matching statistics and reports
- **🔒 Secure Authentication**: Role-based access control

### Launch Web App
```bash
cd webapp
Launch_WebApp.bat
# Choose option 4 for Enhanced App with chatbot
```

Access: http://localhost:5000
- **Admin Login**: `admin` / `HeartMatch2025!`
- **Features**: Full matching system, chatbot, social worker tools

## 📈 Future Enhancements

- **Mobile App**: On-the-go matching capabilities
- **Integration APIs**: Connect with existing case management systems
- **Advanced Analytics**: Predictive matching algorithms
- **Video Profiles**: Multimedia family presentations

## 🤝 Contributing

We welcome contributions to improve HeartMatch:

1. **Bug Reports**: Help us identify and fix issues
2. **Feature Requests**: Suggest new capabilities
3. **Code Contributions**: Submit improvements
4. **Documentation**: Help improve user guides

## 📞 Support

For technical support or questions:
- **Email**: support@heartmatch.ma.gov
- **Phone**: (617) 555-HEART
- **Documentation**: See docs/ folder for detailed guides

## ⚖️ Legal Notice

This system is designed for use by authorized Massachusetts state employees and licensed child welfare agencies. All data handling must comply with state and federal privacy regulations.

---

**Built with ❤️ for the children of Massachusetts**

*"Every child deserves a loving home, and every family deserves the chance to love."*
