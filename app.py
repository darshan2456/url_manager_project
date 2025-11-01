from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import json
import os
import validators

app = Flask(__name__)

# File to store URLs
URLS_FILE = 'urls.json'

def load_urls():
    """Load URLs from JSON file"""
    if os.path.exists(URLS_FILE):
        try:
            with open(URLS_FILE, 'r') as f:
                data = json.load(f)
                return data.get('active', []), data.get('archived', [])
        except:
            return [], []
    return [], []

def save_urls(active_list, archived_list):
    """Save URLs to JSON file"""
    data = {
        'active': active_list,
        'archived': archived_list
    }
    with open(URLS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load existing URLs when app starts
urls, archived_urls = load_urls()

@app.route('/')
def index():
    return render_template('index.html', urls=urls, archived_urls=archived_urls)

@app.route('/add', methods=['POST'])
def add_url():
    global urls
    
    url = request.form['url']
    tags = request.form.get('tags', '').split(',')
    tags = [tag.strip() for tag in tags if tag.strip()]
    
    # URL validation
    if not validators.url(url):
        return redirect('/')
    
    # Simple scraping - just get title for now
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        title_text = title.text.strip() if title else "No title found"
    except Exception as e:
        title_text = f"Error: {str(e)}"
    
    # Add to our list
    urls.append({
        'url': url,
        'title': title_text,
        'tags': tags
    })
    
    # Save to JSON file
    save_urls(urls, archived_urls)
    
    # Redirect to homepage
    return redirect('/')

@app.route('/delete/<int:url_index>')
def delete_url(url_index):
    global urls
    # Check if index is valid
    if 0 <= url_index < len(urls):
        urls.pop(url_index)
        save_urls(urls, archived_urls)
    return redirect('/')

@app.route('/archive/<int:url_index>')
def archive_url(url_index):
    global urls, archived_urls
    if 0 <= url_index < len(urls):
        # Move from urls to archived_urls
        archived_url = urls.pop(url_index)
        archived_urls.append(archived_url)
        save_urls(urls, archived_urls)
    return redirect('/')

@app.route('/unarchive/<int:url_index>')
def unarchive_url(url_index):
    global urls, archived_urls
    if 0 <= url_index < len(archived_urls):
        # Move from archived_urls back to urls
        unarchived_url = archived_urls.pop(url_index)
        urls.append(unarchived_url)
        save_urls(urls, archived_urls)
    return redirect('/')

@app.route('/remove-tag/<int:url_index>/<tag>')
def remove_tag(url_index, tag):
    global urls
    if 0 <= url_index < len(urls):
        # Remove the tag from the URL's tags list
        if tag in urls[url_index]['tags']:
            urls[url_index]['tags'].remove(tag)
            save_urls(urls, archived_urls)
    
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)