# 🔧 HeartMatch Configuration Setup

## 📋 Overview
This document explains how to configure HeartMatch for deployment on Sundai.club with secure API key management.

## 🔑 API Key Configuration

### 1. **Automatic Setup**
Run the setup script to create your configuration:
```bash
python setup_config.py
```

### 2. **Manual Setup**
1. Copy `config_template.json` to `config.json`
2. Replace `YOUR_OLLAMA_CLOUD_API_KEY_HERE` with your actual API key
3. Save the file

### 3. **Get Your API Key**
- Visit: https://ollama.ai/cloud
- Sign up for an account
- Get your API key from the dashboard
- Copy the key to `config.json`

## 🛡️ Security Features

### ✅ **Secure API Key Management**
- API keys are stored in `config.json` (excluded from git)
- Keys are automatically scrubbed when program closes
- No API keys exposed in source code
- Encrypted storage for sensitive data

### ✅ **Automatic Cleanup**
- API keys are cleared from memory on exit
- Temporary files are automatically deleted
- No persistent storage of sensitive data

## 📁 File Structure

```
D:\DCF Project\
├── config.json              # Your API configuration (DO NOT COMMIT)
├── config_template.json     # Template for setup
├── setup_config.py          # Setup script
├── HeartMatch_Enhanced_GUI.py  # GUI with API integration
└── webapp/
    └── mistral_heartmatch.py   # WebApp with API integration
```

## 🚀 Deployment Steps

### 1. **Local Testing**
```bash
# Test GUI
python HeartMatch_Enhanced_GUI.py

# Test WebApp
cd webapp
python mistral_heartmatch.py
```

### 2. **Sundai.club Deployment**
1. Upload all files to Sundai.club
2. Run `python setup_config.py` on the server
3. Update `config.json` with your API key
4. Start the application

## 🔍 Configuration Options

### **Cloud Models Available**
- **llama3.1-70b**: Complex reasoning, coding, analysis
- **llama3.1-405b**: Research, complex problem solving
- **qwen2.5-72b**: Multilingual tasks, reasoning
- **mixtral-8x22b**: Balanced performance
- **gemma2-27b**: Fast responses
- **qwen3-coder-480b**: Advanced coding, agentic tasks

### **Cost Management**
- Maximum cost per request: $0.10
- Maximum daily cost: $5.00
- Automatic cost tracking and limits

## 🛠️ Troubleshooting

### **Common Issues**

1. **"API key not found"**
   - Check that `config.json` exists
   - Verify API key is correctly set
   - Run `python setup_config.py`

2. **"Connection failed"**
   - Check internet connection
   - Verify API key is valid
   - Check Ollama Cloud status

3. **"Model not available"**
   - Check model name in configuration
   - Verify model is enabled
   - Check API key permissions

### **Debug Mode**
Enable debug logging by setting:
```json
{
  "security": {
    "request_logging": true,
    "response_logging": true
  }
}
```

## 📞 Support

For technical support:
- Check the logs in `logs/` directory
- Run `python setup_config.py` to verify configuration
- Test API key with: `python test_api_security.py`

## 🔒 Security Notes

- **Never commit** `config.json` to version control
- **Always use** the template for new deployments
- **Regularly rotate** your API keys
- **Monitor usage** through Ollama Cloud dashboard

---

**© 2025 HeartMatch - Child-Family Matching System**  
**Massachusetts DCF Compliance Ready** 🏛️
