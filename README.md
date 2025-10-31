# 🔗 URL Manager

A simple and powerful web application to save, organize, and manage your website links. Never lose track of important URLs again!

## 🌟 What Can You Do?

### ✨ Save Website Links
- **Add any website URL** - Just paste the link and we'll automatically fetch the page title
- **One-click access** - Click any saved URL to visit the website directly
- **Automatic organization** - Your links are neatly organized with their titles

### 📁 Organize with Archive
- **Archive links you don't need right now** - Hide URLs without deleting them
- **Restore archived links anytime** - Bring back archived URLs with one click
- **Clean separation** - Active and archived URLs are clearly separated

### 🗑️ Safe Management
- **Delete unwanted URLs** - Remove links you no longer need
- **Confirmation before deleting** - Prevent accidental deletions
- **Permanent storage** - Your URLs are saved and won't disappear

## 🚀 How to Use

### Getting Started
1. **Visit the homepage** - You'll see a simple form at the top
2. **Add your first URL** - Paste a website address like `https://example.com`
3. **Watch it appear** - The page title is automatically fetched and displayed

### Managing Your URLs
- **To visit a website**: Click on any URL in your list
- **To archive a URL**: Click the blue "Archive" button
- **To restore an archived URL**: Click the green "Unarchive" button in the archived section
- **To delete a URL**: Click the red "Delete" button (with confirmation)

### Pro Tips
- **Refresh safely** - You can refresh the page anytime without losing data or seeing warnings
- **Your data is safe** - URLs are saved automatically and persist between browser sessions
- **Visual feedback** - Archived URLs appear faded so you can easily distinguish them

## 🛠️ For Developers

### Technical Architecture

This application is built using a modern web development approach:

#### Backend (Python/Flask)
- **Web Framework**: Flask - handles all web requests and routing
- **URL Processing**: 
  - Receives URLs from web forms
  - Uses BeautifulSoup to extract page titles automatically
  - Implements proper error handling for invalid URLs
- **Data Storage**: JSON file system for persistent data storage
- **Routing System**: 
  - `GET /` - Display all URLs (active and archived)
  - `POST /add` - Process new URL submissions
  - `GET /delete/<id>` - Remove URLs with index-based identification
  - `GET /archive/<id>` - Move URLs to archive
  - `GET /unarchive/<id>` - Restore URLs from archive

#### Frontend (HTML/CSS/Jinja2)
- **Templating Engine**: Jinja2 for dynamic HTML generation
- **Responsive Design**: Clean CSS styling that works on all devices
- **User Experience**:
  - Color-coded buttons (red for delete, blue for archive, green for unarchive)
  - Hover effects for better interaction feedback
  - Confirmation dialogs for destructive actions
  - Visual distinction between active and archived items

#### Key Technical Features

**Data Persistence**
- Dual-list system: Active URLs and Archived URLs stored separately
- JSON file structure maintains both lists with automatic saving
- Data survives server restarts and browser sessions

**User Experience Patterns**
- **POST-Redirect-GET Pattern**: Prevents browser refresh warnings after form submissions
- **Progressive Enhancement**: Works without JavaScript for core functionality
- **Error Resilience**: Graceful handling of network issues during URL scraping

**Security & Validation**
- Input validation for URL formats
- Index bounds checking to prevent invalid operations
- Safe data handling with proper error boundaries

### Development Setup

```bash
# Install dependencies
pip install flask beautifulsoup4 requests validators

# Run the application
python app.py

# Access at http://localhost:5000
```

### Project Structure
```
url_manager/
├── app.py                 # Main Flask application
├── urls.json             # Data storage (auto-generated)
├── templates/
│   └── index.html        # Main web interface
└── static/
    └── style.css         # Styling and visual design
```

## 🔧 Technical Details

### Data Flow Architecture
1. **User Input** → Web form submission
2. **URL Validation** → Checks for valid URL format
3. **Content Scraping** → Automatically extracts page title
4. **Data Storage** → Saves to structured JSON file
5. **UI Update** → Displays in appropriate section (active/archived)

### Storage System
- **File-based JSON storage** for simplicity and portability
- **Automatic backup** - data persists through application restarts
- **Scalable structure** - easily extendable for additional features

### Error Handling
- **Network timeouts** for URL scraping (5-second limit)
- **Invalid URL detection** with user-friendly error messages
- **Missing page titles** handled gracefully with fallback text
- **File system errors** managed with appropriate fallbacks

## 📈 Future Enhancements

Planned features include:
- Search and filter functionality
- URL categories and tags
- Bulk operations
- Export capabilities
- User accounts and synchronization

---

**URL Manager** - Your simple, reliable solution for website link management! 🌐