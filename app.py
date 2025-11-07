import os
import flask
from flask import Flask, render_template, request, redirect, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import validators 

app = Flask(__name__)

# ✅ PRODUCTION-READY DATABASE CONFIG
def get_database_uri():
    if 'DATABASE_URL' in os.environ:
        # Production - PostgreSQL (Render)
        uri = os.environ['DATABASE_URL']
        if uri.startswith('postgres://'):
            uri = uri.replace('postgres://', 'postgresql://', 1)
        return uri
    else:
        # Development - SQLite (temporary)
        return 'sqlite:///url_manager.db'

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ MODELS (TERA EXISTING CODE - BILKUL SAME)
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(200))
    is_archived = db.Column(db.Boolean, default=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    color = db.Column(db.String(7))

class URLTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

# ✅ AUTO CREATE TABLES & TAGS
@app.route('/start')
def initialize():
    try:
        db.create_all()
        print("✅ Database tables created")
        
        # Auto-create tags
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
                print(f"✅ Tag created: {name}")
        
        db.session.commit()
        print("✅ Tags initialized successfully!")
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        db.session.rollback()

# ✅ SEARCH FUNCTIONALITY ADDED - TERA EXISTING INDEX ROUTE MODIFIED
@app.route('/')
@app.route('/search')  # Dono routes handle karega
def index():
    search_query = request.args.get('q', '').strip()
    
    # Search BOTH active and archived URLs
    if search_query and not search_query.isspace():
        # Active URLs that match search
        active_results = URL.query.filter(
            db.or_(
                URL.title.ilike(f'%{search_query}%'),
                URL.url.ilike(f'%{search_query}%')
            )
        ).filter_by(is_archived=False).all()
        
        # Archived URLs that match search  
        archived_results = URL.query.filter(
            db.or_(
                URL.title.ilike(f'%{search_query}%'),
                URL.url.ilike(f'%{search_query}%')
            )
        ).filter_by(is_archived=True).all()
        
        is_searching = True
    else:
        # No search - show all active and archived separately
        active_results = URL.query.filter_by(is_archived=False).all()
        archived_results = URL.query.filter_by(is_archived=True).all()
        is_searching = False
    
    # Convert to dict (TERA EXISTING CODE)
    def convert_to_dict(urls):
        result = []
        for url in urls:
            url_tags = URLTag.query.filter_by(url_id=url.id).all()
            tag_names = []
            for url_tag in url_tags:
                tag = Tag.query.get(url_tag.tag_id)
                if tag:
                    tag_names.append(tag.name)
            result.append({
                'id': url.id,
                'url': url.url,
                'title': url.title,
                'tags': tag_names
            })
        return result
    
    active_urls = convert_to_dict(active_results)
    archived_urls = convert_to_dict(archived_results)
    
    # Tag colors for display
    tag_colors = {
        'work': '#3B82F6',
        'programming': '#10B981',
        'research': '#8B5CF6',
        'personal': '#F59E0B',
        'news': '#EF4444'
    }
    
    return render_template('index.html', 
                         urls=active_urls,
                         archived_urls=archived_urls,
                         search_query=search_query,
                         is_searching=is_searching,
                         tag_colors=tag_colors)

# ✅ TERA EXISTING ROUTES - BILKUL SAME RAHEGA
@app.route('/add', methods=['POST'])
def add_url():
    try:
        url = request.form['url']
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        print(f"🎯 DEBUG: URL: {url}, Tags: {tags}")
        
        if not validators.url(url):
            flash('please enter a valid url (e,g - https://example.com)','error')
            return redirect('/')
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
        print(f"✅ URL {url_id} archived")
    return redirect('/')

@app.route('/unarchive/<int:url_id>', methods=['POST'])
def unarchive_url(url_id):
    url = URL.query.get(url_id)  
    if url:
        url.is_archived = False
        db.session.commit()
        print(f"✅ URL {url_id} unarchived")
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)