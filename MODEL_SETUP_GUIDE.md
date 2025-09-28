# 🤖 HeartMatch Model Setup Guide

## 📋 **Overview**
This guide explains how to set up AI models for HeartMatch deployment on Sundai.club.

## 🎯 **Two Deployment Options**

### **Option 1: Local Models (Recommended for Sundai.club)**
- **Download models locally** using Ollama
- **No API keys required** for basic functionality
- **Offline capable** - works without internet
- **Models needed**: `mistral:7b`, `qwen2.5:7b`, `llama2:7b`

### **Option 2: Cloud Models (Advanced)**
- **Use cloud API** with API keys
- **Access to larger models** (70B, 405B, 480B parameters)
- **Requires API key** configuration
- **Costs money** per request

## 🚀 **Quick Setup (Local Models)**

### **Step 1: Install Ollama**
```bash
# Download from: https://ollama.ai/download
# Install and start Ollama service
```

### **Step 2: Download Models**
```bash
# Run the model downloader
python download_models.py
```

### **Step 3: Verify Setup**
```bash
# Test the models
python HeartMatch_Enhanced_GUI.py
```

## 📥 **Model Download Process**

### **Required Models (12.3GB total)**
- **mistral:7b** - 4.1GB - Fast, good for real-time chat
- **qwen2.5:7b** - 4.4GB - Advanced reasoning, best for matching
- **llama2:7b** - 3.8GB - Reliable fallback model

### **Optional Models (for enhanced performance)**
- **qwen2.5:14b** - 8.8GB - Better reasoning
- **qwen2.5:32b** - 20GB - Excellent reasoning
- **llama3:8b** - 4.7GB - Latest Llama model
- **llama3:13b** - 7.3GB - High performance

## 🔧 **Manual Model Download**

If the automatic downloader doesn't work:

```bash
# Download required models
ollama pull mistral:7b
ollama pull qwen2.5:7b
ollama pull llama2:7b

# Optional: Download larger models
ollama pull qwen2.5:14b
ollama pull llama3:8b
```

## 🌐 **Cloud Model Setup (Optional)**

### **Step 1: Get API Key**
1. Visit: https://ollama.ai/cloud
2. Sign up for account
3. Get your API key

### **Step 2: Configure API Key**
```bash
# Run configuration setup
python setup_config.py
```

### **Step 3: Update config.json**
```json
{
  "ollama_cloud": {
    "api_key": "YOUR_ACTUAL_API_KEY_HERE"
  }
}
```

## 📁 **File Structure**

```
D:\DCF Project\
├── models/
│   ├── model_manager.py          # Model management utilities
│   └── model_config.json         # Model configuration
├── config.json                   # API configuration (if using cloud)
├── config_template.json          # Template for new deployments
├── download_models.py            # Model downloader script
├── setup_config.py              # Configuration setup
└── HeartMatch_Enhanced_GUI.py   # Main GUI application
```

## 🛠️ **Troubleshooting**

### **"Ollama not found"**
- Install Ollama from https://ollama.ai/download
- Add Ollama to your PATH
- Restart command prompt

### **"Ollama service not running"**
- Start Ollama service: `ollama serve`
- Or start from Start Menu
- Check if port 11434 is available

### **"Model download failed"**
- Check internet connection
- Ensure enough disk space (12GB+)
- Try downloading models one by one

### **"Model not responding"**
- Check if model is installed: `ollama list`
- Restart Ollama service
- Check model name spelling

## 📊 **Model Performance Comparison**

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| mistral:7b | 4.1GB | ⚡⚡⚡ | ⭐⭐⭐ | Real-time chat |
| qwen2.5:7b | 4.4GB | ⚡⚡ | ⭐⭐⭐⭐ | Matching, reasoning |
| llama2:7b | 3.8GB | ⚡⚡ | ⭐⭐⭐ | General tasks |
| qwen2.5:14b | 8.8GB | ⚡ | ⭐⭐⭐⭐⭐ | Complex analysis |
| llama3:8b | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | Latest features |

## 🚀 **Sundai.club Deployment**

### **For Local Models Only:**
1. ✅ Download models locally
2. ✅ Upload all files to Sundai.club
3. ✅ Install Ollama on server
4. ✅ Run `ollama serve` on server
5. ✅ Start HeartMatch application

### **For Cloud Models:**
1. ✅ Upload all files to Sundai.club
2. ✅ Run `python setup_config.py`
3. ✅ Update `config.json` with API key
4. ✅ Start HeartMatch application

## 💡 **Recommendations**

### **For Sundai.club (Recommended):**
- **Use local models** for reliability
- **Start with mistral:7b** for basic functionality
- **Add qwen2.5:7b** for better matching
- **Keep llama2:7b** as fallback

### **For Development:**
- **Use cloud models** for testing
- **Access larger models** for complex tasks
- **Monitor API costs** carefully

## 🔒 **Security Notes**

- **Local models**: No API keys needed, completely private
- **Cloud models**: API keys required, monitor usage
- **Hybrid mode**: Best of both worlds
- **Offline capable**: Works without internet

---

**© 2025 HeartMatch - Child-Family Matching System**  
**Massachusetts DCF Compliance Ready** 🏛️

**Status**: ✅ **READY FOR DEPLOYMENT** 🚀
