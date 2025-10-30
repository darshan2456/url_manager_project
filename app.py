from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

# File to store URLs
URLS_FILE = 'urls.json'

def load_urls():
    """Load URLs from JSON file"""
    if os.path.exists(URLS_FILE):
        try:
            with open(URLS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_urls(urls_list):
    """Save URLs to JSON file"""
    with open(URLS_FILE, 'w') as f:
        json.dump(urls_list, f, indent=2)

# Load existing URLs when app starts
urls = load_urls()



@app.route('/')
def index():
    return render_template('index.html', urls=urls)

@app.route('/add', methods=['POST'])
def add_url():
    url = request.form['url']
    
    # Simple scraping - just get title for now
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        title_text = title.text.strip() if title else "No title found"
    except Exception as e:
        title_text = f"Error: {str(e)}"
    
    # Add to our list
    urls.append({
        'url': url,
        'title': title_text
    })
    
    save_urls(urls)
    
    # Go back to homepage which will show updated list
    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)