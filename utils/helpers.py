from models import db
from models.page import Page, Post, SocialMediaUser

def store_page_data(page_data, posts_data, employees_data):
    page = Page.query.filter_by(linkedin_id=page_data['linkedin_id']).first()
    if not page:
        page = Page(**page_data)
        db.session.add(page)
    else:
        for key, value in page_data.items():
            setattr(page, key, value)
    
    db.session.commit()
    
    for post_item in posts_data:
        post = Post.query.filter_by(linkedin_post_id=post_item['linkedin_post_id']).first()
        if not post:
            post = Post(**post_item, page=page)
            db.session.add(post)
    
    for emp_item in employees_data:
        employee = SocialMediaUser.query.filter_by(name=emp_item['name']).first()
        if not employee:
            employee = SocialMediaUser(**emp_item, page=page)
            db.session.add(employee)
    
    db.session.commit()
    return page