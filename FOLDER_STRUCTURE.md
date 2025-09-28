# 📁 HeartMatch Project Structure

## 🗂️ **Organized Folder Structure**

```
D:\DCF Project\
├── 📁 webapp/                          # Web Application
│   ├── 📄 sundai_deployment.py         # 🌐 Sundai.club deployment (8B models)
│   ├── 📄 clean_working_app.py          # 🧹 Clean working app (JSON safe)
│   ├── 📄 basic_app.py                 # 🔧 Basic demo app
│   ├── 📄 main_app.py                  # 🚀 Full production app
│   ├── 📄 Launch_Sundai_Deployment.bat # 🚀 Sundai launcher
│   ├── 📄 Launch_WebApp.bat           # 🚀 General launcher
│   ├── 📄 launch.py                    # 🐍 Python launcher
│   ├── 📄 requirements.txt             # 📦 Dependencies
│   ├── 📄 README.md                    # 📖 Documentation
│   ├── 📁 static/                      # 🎨 Static assets
│   │   ├── 📁 css/
│   │   │   └── 📄 style.css
│   │   └── 📁 js/
│   │       └── 📄 app.js
│   ├── 📁 templates/                   # 📄 HTML templates
│   │   ├── 📁 auth/
│   │   │   └── 📄 login.html
│   │   ├── 📄 base.html
│   │   ├── 📄 index.html
│   │   ├── 📄 dashboard.html
│   │   └── 📄 matching.html
│   └── 📁 uploads/                     # 📁 Secure uploads
│
├── 📁 secure_features/                 # 🔒 Security & Compliance
│   ├── 📄 psychological_profiling.py   # 🧠 Myers-Briggs & Big Five
│   ├── 📄 pdf_handler.py              # 📄 Secure PDF processing
│   ├── 📄 ada_compliance.py           # ♿ ADA compliance
│   └── 📄 compassionate_chatbot.py     # 💙 Emotional support bot
│
├── 📄 HeartMatch_Psychological_GUI.py  # 🖥️ GUI Application
├── 📄 HeartMatch_Child_Family_Matching_System.py # 🔧 Original system
├── 📄 Launch_HeartMatch.bat           # 🚀 GUI launcher
├── 📄 test_heartmatch.py              # 🧪 GUI tests
├── 📄 test_simple_webapp.py           # 🧪 Web app tests
└── 📄 FOLDER_STRUCTURE.md             # 📖 This file
```

## 🚀 **Deployment Options**

### **1. Sundai.club Deployment (Recommended)**
```bash
cd webapp
Launch_Sundai_Deployment.bat
```
- ✅ **8B AI Models** - No API keys required
- ✅ **DCF Calendar** - Massachusetts events
- ✅ **Privacy First** - Local processing
- ✅ **Production Ready** - Optimized for Sundai.club

### **2. Clean Working App**
```bash
cd webapp
Launch_WebApp.bat
# Choose option 1
```
- ✅ **JSON Safe** - Perfect serialization
- ✅ **Compassionate Chat** - Emotional support
- ✅ **No Dependencies** - Works immediately

### **3. GUI Application**
```bash
python HeartMatch_Psychological_GUI.py
```
- ✅ **Psychological Profiling** - Myers-Briggs analysis
- ✅ **PDF Processing** - Secure document handling
- ✅ **ADA Compliant** - Full accessibility
- ✅ **Compassionate Chat** - Emotional support

## 🎯 **Key Features by Deployment**

### **Sundai.club Deployment:**
- 🤖 **8B AI Models** - Advanced local processing
- 📅 **DCF Calendar** - Massachusetts events integration
- 🔒 **Privacy First** - No external API keys
- 💙 **Compassionate Chat** - Emotional support
- 📊 **Dashboard** - Complete overview

### **Clean Working App:**
- 🧹 **JSON Safe** - Perfect serialization
- 💙 **Compassionate Chat** - Emotional support
- 📊 **Dashboard** - Statistics and overview
- 🔍 **Health Check** - System status

### **GUI Application:**
- 🧠 **Psychological Profiling** - Myers-Briggs & Big Five
- 📄 **PDF Processing** - Secure document handling
- ♿ **ADA Compliance** - Full accessibility
- 💙 **Compassionate Chat** - Emotional support
- 🔒 **Security Features** - Enterprise-grade

## 📞 **Massachusetts DCF Resources**

### **Crisis Support:**
- 🆘 **Emergency:** 911
- 🆘 **Suicide Prevention:** 988
- 🆘 **Child Abuse Hotline:** 1-800-4-A-CHILD

### **DCF Resources:**
- 📞 **DCF Hotline:** 1-800-792-5200
- 📞 **Foster Care Support:** 1-800-394-3366
- 🌐 **Mental Health:** mass.gov/mental-health

### **DCF Events Calendar:**
- 📅 **Training Sessions** - Monthly foster parent training
- 📅 **Information Nights** - Adoption process information
- 📅 **Support Groups** - Monthly family support
- 📅 **Workshops** - Child safety and trauma care
- 📅 **Celebrations** - Annual appreciation events

## 🔧 **Technical Specifications**

### **AI Models:**
- **8B Parameters** - Advanced local processing
- **No API Keys** - Complete privacy
- **Local Processing** - Maximum security
- **Compassionate Responses** - Emotional support

### **Security:**
- **PII Protection** - Massachusetts compliance
- **Encrypted Communications** - Secure data
- **ADA Compliance** - Full accessibility
- **Privacy First** - No external dependencies

### **Features:**
- **Child-Family Matching** - AI-powered compatibility
- **Psychological Profiling** - Myers-Briggs analysis
- **Document Processing** - Secure PDF handling
- **Event Calendar** - DCF events integration
- **Compassionate Chat** - Emotional support

## 🎯 **Quick Start Guide**

1. **Choose your deployment:**
   - **Sundai.club:** `Launch_Sundai_Deployment.bat`
   - **Clean App:** `Launch_WebApp.bat` → Option 1
   - **GUI:** `python HeartMatch_Psychological_GUI.py`

2. **Access the system:**
   - **Web:** http://localhost:5000
   - **Dashboard:** http://localhost:5000/dashboard
   - **Chat:** http://localhost:5000/chatbot
   - **Calendar:** http://localhost:5000/calendar

3. **Use the features:**
   - **AI Matching** - Find compatible families
   - **Compassionate Chat** - Emotional support
   - **DCF Calendar** - Massachusetts events
   - **Psychological Analysis** - Advanced profiling

## 📞 **Support**

For technical support or questions about the HeartMatch system, refer to the individual README files in each folder or contact the development team.
