def scrape_linkedin_page(page_id):
   
    page_data = {
        'linkedin_id': page_id,
        'page_name': f"Demo Page {page_id}",
        'page_url': f"https://www.linkedin.com/company/{page_id}/",
        'profile_picture': f"https://dummyimage.com/200x200/000/fff&text={page_id}",
        'description': f"This is a description for {page_id}.",
        'website': f"https://www.{page_id}.com",
        'industry': "Technology",
        'total_followers': 25000,
        'head_count': 150,
        'specialities': "Software, Engineering, Consulting"
    }
    
    posts = [{'linkedin_post_id': f"{page_id}post{i}", 'content': f"Content of post {i}"} for i in range(1, 16)]
    employees = [{'name': f"Employee {i}", 'profile_picture': "https://dummyimage.com/100x100/000/fff", 'designation': "Engineer", 'linkedin_profile': f"https://www.linkedin.com/in/employee{i}_{page_id}"} for i in range(1, 3)]
    
    return page_data, posts, employees