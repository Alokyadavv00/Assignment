# LinkedIn Insights Microservice

This is a Flask-based microservice for fetching and storing LinkedIn page insights.

## Features

- Scrape LinkedIn page details and store them in a database.
- Retrieve page details, posts, and comments via RESTful API endpoints.
- Filter pages by follower count, name, and industry.
- Pagination support for posts and comments.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/linkedin_insights.git
   cd linkedin_insights

2. **Create a virtual environment**:
python -m venv venv
source venv/bin/activate  
# On Windows use `venv\Scripts\activate`

3. **Install dependencies**:
pip install -r requirements.txt

4. **Configure environment variables**:
Copy .env.example to .env and fill in the necessary values.

5. **Run the application**:
python app.py

**Usage**
Access the API at http://localhost:5000.
Use tools like Postman to test the endpoints.

**API Endpoints**

1. Welcome Endpoint: GET /
Returns a welcome message.

2. Get Page Details: GET /page/<page_id>
Retrieves detailed information about a LinkedIn page by its ID. Scrapes and stores data if not found in the database.

3. Get Pages with Filters: GET /pages
Retrieves a list of LinkedIn pages with optional filters for follower count, name, and industry. Supports pagination.

4. Get Page Posts: GET /page/<page_id>/posts
Retrieves posts for a specific LinkedIn page. Supports pagination.

5. Get Post Comments: GET /page/<page_id>/posts/<linkedin_post_id>/comments
Retrieves comments for a specific post on a LinkedIn page.

**Usage**
Access the API at http://localhost:5000.
Use tools like Postman to test the endpoints.

**Contributing**
Contributions are welcome! Please open an issue or submit a pull request.