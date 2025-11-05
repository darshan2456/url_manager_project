from flask import Flask, render_template, request, redirect, jsonify
import flask_sqlalchemy
import requests
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import os


db_path = os.path.join(os.getcwd(), 'url_manager.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 1. URL Class
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(200))
    is_archived = db.Column(db.Boolean, default=False)

# 2. Tag Class
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    color = db.Column(db.String(7))

# 3. URLTag Class
class URLTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))



@app.route('/')
def index():
    active_urls_db = URL.query.filter_by(is_archived=False).all()
    archived_urls_db = URL.query.filter_by(is_archived=True).all()
    
    def convert_to_dict(urls):
        result = []
        for url in urls:
            url_tags = URLTag.query.filter_by(url_id=url.id).all()
            print(f"🔄 URL {url.id} - Found {len(url_tags)} URLTag records")  # Debug
        
            tag_names = []
            for url_tag in url_tags:
                tag = Tag.query.get(url_tag.tag_id)
                print(f"   Tag ID {url_tag.tag_id} -> {tag.name if tag else 'NOT FOUND'}")  # Debug
                if tag:
                    tag_names.append(tag.name)
        
            result.append({
                'id': url.id,
                'url': url.url,
                'title': url.title,
                'tags': tag_names
            })
        return result
    
    active_urls = convert_to_dict(active_urls_db)
    archived_urls = convert_to_dict(archived_urls_db)
    
    return render_template('index.html', urls=active_urls, archived_urls=archived_urls)
    

@app.route('/add', methods=['POST'])
def add_url():
    try:
        url = request.form['url']
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        print(f"🎯 DEBUG: URL: {url}, Tags: {tags}")
        
        # ✅ SAFE TITLE FETCHING
        title_text = "No title"  # Default value
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=5, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title')
            title_text = title.text.strip() if title else "No title found"
        except Exception as e:
            title_text = f"Error: {str(e)}"
        
        print(f"🎯 DEBUG: Title: {title_text}")
        
        # Create URL (ab title_text always defined hai)
        new_url = URL(url=url, title=title_text)
        db.session.add(new_url)
        db.session.flush()
        
        print(f"🎯 DEBUG: URL ID: {new_url.id}")
        
        # Add tags
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            print(f"🎯 DEBUG: Tag '{tag_name}' found: {tag is not None}")
            
            if tag:
                url_tag = URLTag(url_id=new_url.id, tag_id=tag.id)
                db.session.add(url_tag)
        
        db.session.commit()
        print(f"✅ URL added with {len(tags)} tags")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error adding URL: {e}")
    
    return redirect('/')

@app.route('/delete/<int:url_id>', methods=['POST'])
def delete_url(url_id):
    try:
        # 1. Pehle URLTags delete karo (foreign key constraint)
        URLTag.query.filter_by(url_id=url_id).delete()
        
        # 2. Phir URL delete karo
        url = URL.query.get(url_id)
        if url:
            db.session.delete(url)
            db.session.commit()
            print(f"✅ URL {url_id} deleted successfully")
        else:
            print(f"❌ URL {url_id} not found")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error deleting URL {url_id}: {e}")
    
    return redirect('/')

@app.route('/archive/<int:url_id>', methods=['POST'])
def archive_url(url_id):
    url = URL.query.get(url_id)
    if url:
        url.is_archived = True
        db.session.commit()
    return redirect('/')

@app.route('/unarchive/<int:url_id>', methods=['POST'])
def unarchive_url(url_id):
    url = URL.query.get(url_id)  
    if url:
        url.is_archived = False
        db.session.commit()
    return redirect('/')

@app.route('/remove-tag/<int:url_id>/<tag>')
def remove_tag(url_id, tag):
    try:
        # Find the tag
        tag_obj = Tag.query.filter_by(name=tag).first()
        if tag_obj:
            # Remove the relationship
            url_tag = URLTag.query.filter_by(url_id=url_id, tag_id=tag_obj.id).first()
            if url_tag:
                db.session.delete(url_tag)
                db.session.commit()
                print(f"✅ Tag '{tag}' removed from URL {url_id}")
            else:
                print(f"❌ Tag relationship not found")
        else:
            print(f"❌ Tag '{tag}' not found")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error removing tag: {e}")
    
    return redirect('/')


# Temporary route to insert tags
@app.route('/init-tags')
def init_tags():
    tags_data = [
        ('work', '#3B82F6'),
        ('programming', '#10B981'),
        ('research', '#8B5CF6'),
        ('personal', '#F59E0B'),
        ('news', '#EF4444')
    ]
    
    for name, color in tags_data:
        if not Tag.query.filter_by(name=name).first():
            tag = Tag(name=name, color=color)
            db.session.add(tag)
    
    db.session.commit()
    return "Tags initialized!"
    
    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)