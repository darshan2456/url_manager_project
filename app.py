from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Temporary storage (we'll replace with database later)
urls = []

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
    
    # Go back to homepage which will show updated list
    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)