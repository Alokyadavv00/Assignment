from . import db

class Page(db.Model):
    _tablename_ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    linkedin_id = db.Column(db.String(255), unique=True, nullable=False)
    page_name = db.Column(db.String(255))
    page_url = db.Column(db.String(500))
    profile_picture = db.Column(db.String(500))
    description = db.Column(db.Text)
    website = db.Column(db.String(500))
    industry = db.Column(db.String(255))
    total_followers = db.Column(db.Integer)
    head_count = db.Column(db.Integer)
    specialities = db.Column(db.Text)
    
    # Relationships
    posts = db.relationship("Post", backref="page", cascade="all, delete-orphan")
    employees = db.relationship("SocialMediaUser", backref="page", cascade="all, delete-orphan")


class Post(db.Model):
    _tablename_ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    linkedin_post_id = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    
    # Relationship: a post can have multiple comments
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")


class Comment(db.Model):
    _tablename_ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    posted_by = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class SocialMediaUser(db.Model):
    _tablename_ = 'social_media_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    profile_picture = db.Column(db.String(500))
    designation = db.Column(db.String(255))
    linkedin_profile = db.Column(db.String(500))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))