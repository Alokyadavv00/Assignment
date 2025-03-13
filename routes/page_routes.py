from flask import Blueprint, request, jsonify
from models import db
from models.page import Page, Post, Comment, SocialMediaUser
from services.scraper import scrape_linkedin_page
from utils.helpers import store_page_data
import openai
from flask import current_app

bp = Blueprint('page_routes', __name__)


@bp.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to LinkedIn Insights API. Use /page/<page_id> for details.'})

# Get Page Details endpoint
@bp.route('/page/<string:page_id>', methods=['GET'])
def get_page_details(page_id):
    page = Page.query.filter_by(linkedin_id=page_id).first()
    if not page:
        page_data, posts_data, employees_data = scrape_linkedin_page(page_id)
        page = store_page_data(page_data, posts_data, employees_data)
    
    response = {
        'linkedin_id': page.linkedin_id,
        'page_name': page.page_name,
        'page_url': page.page_url,
        'profile_picture': page.profile_picture,
        'description': page.description,
        'website': page.website,
        'industry': page.industry,
        'total_followers': page.total_followers,
        'head_count': page.head_count,
        'specialities': page.specialities,
        'posts': [{'linkedin_post_id': post.linkedin_post_id, 'content': post.content} for post in page.posts],
        'employees': [{'name': emp.name, 'profile_picture': emp.profile_picture, 'designation': emp.designation, 'linkedin_profile': emp.linkedin_profile} for emp in page.employees]
    }
    return jsonify(response)

# Filter Pages endpoint
@bp.route('/pages', methods=['GET'])
def get_pages():
    min_followers = request.args.get('min_followers', type=int)
    max_followers = request.args.get('max_followers', type=int)
    name = request.args.get('name', type=str)
    industry = request.args.get('industry', type=str)
    
    query = Page.query
    if min_followers is not None:
        query = query.filter(Page.total_followers >= min_followers)
    if max_followers is not None:
        query = query.filter(Page.total_followers <= max_followers)
    if name:
        query = query.filter(Page.page_name.ilike(f'%{name}%'))
    if industry:
        query = query.filter(Page.industry.ilike(f'%{industry}%'))
    
    page_number = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    paginated = query.paginate(page=page_number, per_page=per_page, error_out=False)
    
    pages = [{
        'linkedin_id': p.linkedin_id,
        'page_name': p.page_name,
        'page_url': p.page_url,
        'total_followers': p.total_followers,
        'industry': p.industry
    } for p in paginated.items]
    
    return jsonify({
        'pages': pages,
        'total': paginated.total,
        'page': paginated.page,
        'pages_count': paginated.pages
    })

# Get Recent Posts endpoint
@bp.route('/page/<string:page_id>/posts', methods=['GET'])
def get_page_posts(page_id):
    page = Page.query.filter_by(linkedin_id=page_id).first()
    if not page:
        return jsonify({'error': 'Page not found'}), 404

    page_number = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    posts_query = Post.query.filter_by(page_id=page.id).order_by(Post.id.desc())
    paginated_posts = posts_query.paginate(page=page_number, per_page=per_page, error_out=False)
    
    posts = [{
        'linkedin_post_id': post.linkedin_post_id,
        'content': post.content,
        'comments_count': len(post.comments)
    } for post in paginated_posts.items]
    
    return jsonify({
        'posts': posts,
        'total': paginated_posts.total,
        'page': paginated_posts.page,
        'pages_count': paginated_posts.pages
    })

# Get Post Comments endpoint
@bp.route('/page/<string:page_id>/posts/<string:linkedin_post_id>/comments', methods=['GET'])
def get_post_comments(page_id, linkedin_post_id):
    page = Page.query.filter_by(linkedin_id=page_id).first()
    if not page:
        return jsonify({'error': 'Page not found'}), 404

    post = Post.query.filter_by(linkedin_post_id=linkedin_post_id, page=page).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    comments = [{
        'id': comment.id,
        'content': comment.content,
        'posted_by': comment.posted_by
    } for comment in post.comments]

    return jsonify({'post': linkedin_post_id, 'comments': comments})


openai.api_key = "Api Key" 

@bp.route('/page/<string:page_id>/summary', methods=['GET'])
def get_page_summary(page_id):
    page = Page.query.filter_by(linkedin_id=page_id).first()
    if not page:
        return jsonify({'error': 'Page not found'}), 404

    prompt = (
        f"Summarize the LinkedIn page '{page.page_name}' in the {page.industry} industry. "
        f"Key details: {page.total_followers} followers, {page.head_count} employees. "
        f"Description: {page.description}"
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    summary = response.choices[0].message['content']
    return jsonify({'page_id': page_id, 'summary': summary})