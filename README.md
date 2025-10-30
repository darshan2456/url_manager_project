# URL Manager

A simple web application that helps you save and organize website links. 

## What It Does

- **Save Website Links**: Add any website URL and the app automatically fetches the page title
- **Never Lose Your Links**: Your saved URLs are stored safely and won't disappear when you close the app
- **Clean Interface**: Simple and easy-to-use design
- **One-Click Access**: Click on any saved URL to visit the website directly

## How to Use

1. **Add a URL**: Type any website address (like `https://example.com`) in the box and click "Add URL"
2. **View Your Links**: See all your saved URLs with their page titles in a clean list
3. **Visit Websites**: Click on any URL in your list to open that website

## Technical Stuff (For Developers)

This is built with:
- **Flask** - The web framework that makes it all work
- **BeautifulSoup** - Extracts page titles from websites  
- **JSON File Storage** - Saves your URLs so they persist between app restarts

## Getting Started

```bash
# Install required packages
pip install flask beautifulsoup4 requests

# Run the application
python app.py
```

Then open your browser and go to `http://localhost:5000`

## Project Status

✅ **Working Features**:
- Add URLs with automatic title fetching
- Persistent storage using JSON file
- Clean web interface

🔄 **Coming Soon**:
- Delete unwanted URLs
- Archive feature
- Better organization options

This project started as a learning exercise and has grown into a useful tool for managing web links!