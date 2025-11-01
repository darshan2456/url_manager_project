```markdown
# 🔗 URL Manager

A **Flask-based web application** to save, organize, and manage website URLs with smart tagging and archiving capabilities.

## 🌟 **Features**

### 🎯 **Core Functionality**
- ➕ **Add URLs** with automatic title scraping using BeautifulSoup
- 🏷️ **Smart Tagging System** with predefined categories (Work, Programming, Research, Personal)
- 📦 **Archive/Unarchive System** for temporary URL storage
- 💾 **Persistent Storage** using JSON file system
- ✅ **URL Validation** using Python's validators library

### 🎨 **Tag Management**
- 🌈 **Color-coded tags** for visual organization
- 📊 **Tag sidebar** for quick filtering and navigation
- ❌ **Remove tags** from individual URLs
- 🔍 **Tag-based URL grouping** in sidebar dropdowns

### ✨ **User Experience**
- 📋 **One-click URL copying** with visual feedback
- ⚠️ **Confirmation dialogs** for destructive actions
- 🔄 **POST-Redirect-GET pattern** to prevent browser refresh issues
- 📱 **Responsive design** with clean, modern interface

## 🛠️ **Technical Stack**

### 🔧 **Backend**
- **Framework**: 🐍 Flask (Python)
- **URL Processing**: 🕸️ BeautifulSoup4 for title extraction
- **Validation**: ✅ Python validators library
- **HTTP Requests**: 🌐 Requests library with custom headers
- **Data Storage**: 📁 JSON file-based system

### 🎨 **Frontend**
- **Templating**: Jinja2
- **Styling**: Custom CSS with color-coded tag system
- **Interactivity**: Vanilla JavaScript for tag selection and URL copying
- **Responsive Design**: Flexbox layout

### 💾 **Data Structure**
```json
{
  "active": [
    {
      "url": "https://example.com",
      "title": "Example Domain",
      "tags": ["work", "programming"]
    }
  ],
  "archived": []
}
```

## 📁 **Project Structure**
```
url_manager_project/
├── 🐍 app.py                 # Main Flask application
├── 💾 urls.json             # Auto-generated data storage
├── 🎨 static/
│   ├── style.css         # Comprehensive styling
│   └── script.js         # Frontend interactions
└── 📄 templates/
    └── index.html        # Main template with tag system
```

## 🚀 **Installation & Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/darshan2456/url_manager_project.git
   cd url_manager_project
   ```

2. **Install dependencies**
   ```bash
   pip install flask beautifulsoup4 requests validators
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   ```
   Open your browser and go to: http://localhost:5000
   ```

## 🎮 **How to Use**

### **Adding URLs**
1. Enter a URL in the input field
2. Select relevant tags from the color-coded buttons
3. Click "Add URL" - the title will be automatically fetched!

### **Managing URLs**
- 🔗 **Visit**: Click on any URL to open it
- 📋 **Copy**: Use the "Copy URL" button for quick sharing
- 📦 **Archive**: Click "Archive" to temporarily hide URLs
- 📥 **Unarchive**: Restore from the archived section
- 🗑️ **Delete**: Remove permanently with confirmation
- ❌ **Remove Tags**: Click the × on any tag to remove it

### **Using Tags**
- 🎯 **Filter**: Click tags in the sidebar to view related URLs
- 📊 **Overview**: See tag counts in the sidebar
- 🎨 **Visual Organization**: Colors help quickly identify categories


## 🚀 **Future Enhancements**
- 🔍 Search functionality
- 📁 Custom tag creation
- 👥 User accounts
- 📤 Export capabilities
- 🔄 Bulk operations

---

**⭐ Star this repo if you find it useful!**

**🐛 Found a bug?** Open an issue on GitHub!

**💡 Have a feature request?** We'd love to hear your ideas!
```

This version uses emojis, bold text, and color-coding to make it visually appealing while remaining completely readable as a standard markdown file! 🎉