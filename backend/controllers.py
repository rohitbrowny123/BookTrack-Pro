from flask import  jsonify, request, redirect, url_for, Blueprint , send_file , session
from models import *
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from models import db,Section
from werkzeug.utils import secure_filename
# from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import current_user
from sqlalchemy import func


from tasks import add


bp = Blueprint('main', __name__)

# import jwt
SECRET_KEY = '1234'
# UPLOAD_FOLDER = 'C:\Users\91709\OneDrive\Desktop\myLMS Books'


from datetime import datetime, timedelta
# import jwt


# celery demo
@app.route('/celerydemo')
def celery_demo():
    add.delay(10,20)






# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json()
#         user = User.query.filter_by(username=data['username']).first()
#         if user and check_password_hash(user.password, data['password']):
#             role = 'User'  # Default role
#             if user.roles:
#                 role = user.roles[0].name
            
#             # Generate JWT token
#             token_payload = {
#                 'user_id': user.id,
#                 'username': user.username,
#                 'exp': datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
#             }
#             token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
            
#             return jsonify({
#                 'message': 'Login successful',
#                 'role': role,
#                 'username': user.username,
#                 'token': token
#             }), 200
#         else:
#             return jsonify({'message': 'Invalid username or password'}), 401
#     except Exception as e:
#         print(f"Login error: {str(e)}")
#         return jsonify({'message': 'An error occurred during login'}), 500
    
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            role = 'User'  # Default role
            if user.roles:
                role = user.roles[0].name
            
            return jsonify({
                'message': 'Login successful',
                'role': role,
                'username': user.username,
                'user_id': user.id  # Add this line
            }), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'An error occurred during login'}), 500   


@app.route('/api/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

@app.route('/api/users', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('userType')

    if not username or not email or not password or not user_type:
        return jsonify({'error': 'All fields are required.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    role = Role.query.filter_by(name=user_type).first()
    if not role:
        role = Role(name=user_type, description=f'{user_type} role')
        db.session.add(role)
        db.session.commit()

    new_user.roles.append(role)
    db.session.commit()

    print(f"User created: {new_user.username}, {new_user.email}, Role: {user_type}")

    if user_type == 'Librarian':
        return jsonify({'message': 'Registration successful!', 'username': username, 'redirect': 'LibrarianDashboard'}), 201
    else:
        return jsonify({'message': 'Registration successful!', 'username': username, 'redirect': 'UserDashboard'}), 201


@app.route('/api/users', methods=['GET'])
def fetch_all_users():
    print("Fetching all users...")
    try:
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        print(f"Fetched {len(users_list)} users")
        return jsonify(users_list)
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/test-db')
def test_db():
    try:
        users = User.query.all()
        return jsonify({'message': f'Database connection successful. User count: {len(users)}'}), 200
    except Exception as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500
    
@app.route('/test')
def test_route():
    print("Test route accessed")
    return jsonify({"message": "Test route working"}), 200


@app.route('/test-users')
def test_users():
    try:
        users = User.query.all()
        return jsonify({'message': f'Found {len(users)} users'}), 200
    except Exception as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500

import traceback

@app.route('/api/sections', methods=['GET'])
def get_sections():
    try:
        current_app.logger.info("Fetching sections...")
        sections = Section.query.all()
        sections_data = [section.to_dict() for section in sections]
        current_app.logger.info(f"Fetched {len(sections_data)} sections successfully")
        return jsonify(sections_data), 200
    except Exception as e:
        current_app.logger.error(f"Unexpected error when fetching sections: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            'message': 'Unexpected error when fetching sections', 
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500
    
@app.route('/test-sections')
def test_sections():
    try:
        sections = Section.query.all()
        return jsonify({'message': f'Found {len(sections)} sections', 'sections': [s.to_dict() for s in sections]}), 200
    except Exception as e:
        return jsonify({'message': f'Error testing sections: {str(e)}'}), 500
   
   
@app.route('/test-db-sections')
def test_db_sections():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        
        # Test Section model
        sections = Section.query.all()
        section_data = [{'id': s.id, 'title': s.title} for s in sections]
        
        return jsonify({
            'message': 'Database and Section model test successful',
            'section_count': len(sections),
            'sections': section_data
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'Error testing database and Section model',
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500 
    

@app.route('/api/sections/<int:section_id>', methods=['PUT'])
def update_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"message": "Section not found"}), 404
    
    data = request.form
    try:
        section.title = data.get('title', section.title)
        section.date_created = datetime.strptime(data.get('date_created'), '%Y-%m-%d')
        section.image = data.get('image', section.image)
        section.description = data.get('description', section.description)
        db.session.commit()
        return jsonify(section.to_dict()), 200
    except Exception as e:
        return jsonify({'message': 'Error updating section', 'error': str(e)}), 500

@app.route('/api/sections/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    try:
        section = Section.query.get_or_404(section_id)
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/sections', methods=['POST'])
def add_section():
    data = request.json
    try:
        new_section = Section(
            title=data['title'],
            date_created=datetime.fromisoformat(data['dateCreated']),
            image=data.get('image'),
            description=data['description']
        )
        db.session.add(new_section)
        db.session.commit()
        return jsonify(new_section.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding section: {str(e)}")
        return jsonify({'message': 'Error adding section', 'error': str(e)}), 500
    
    
import os

@app.route('/check-db-file')
def check_db_file():
    db_path = 'instance/database.db'  # Adjust this path if necessary
    if not os.path.exists(db_path):
        return jsonify({'message': f"Database file not found at {db_path}"})
    else:
        return jsonify({
            'message': f"Database file found at {db_path}",
            'permissions': oct(os.stat(db_path).st_mode)[-3:]
        })
        
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    try:
        new_book = Book(
            name=data['name'],
            description=data['description'],
            content=data['content'],
            author=data['author'],
            status=data['status'],
            section_id=data['section_id']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully", "id": new_book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/sections/<int:section_id>', methods=['GET', 'PUT'])
def section_detail(section_id):
    section = Section.query.get_or_404(section_id)
    
    if request.method == 'GET':
        return jsonify(section.to_dict())
    
    elif request.method == 'PUT':
        try:
            section.title = request.form.get('title', section.title)
            section.description = request.form.get('description', section.description)
            section.date_created = datetime.strptime(request.form.get('date_created'), '%Y-%m-%d')

            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    section.image = filename

            db.session.commit()
            return jsonify({"message": "Section updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
        
# @app.route('/api/books', methods=['GET'])
# def get_books():
#     try:
#         books = Book.query.all()
#         books_data = []
#         for book in books:
#             book_dict = book.to_dict()
#             # Ensure all fields are serializable
#             for key, value in book_dict.items():
#                 if not isinstance(value, (str, int, float, bool, type(None))):
#                     book_dict[key] = str(value)
#             books_data.append(book_dict)
#         print(f"Returning {len(books_data)} books: {books_data}")
#         return jsonify(books_data), 200
#     except Exception as e:
#         print(f"Error fetching books: {str(e)}")
#         return jsonify({'message': 'Error fetching books', 'error': str(e)}), 500


@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        books_data = []
        for book in books:
            book_dict = book.to_dict()
            # Fetch the section title
            section = Section.query.get(book.section_id)
            book_dict['section'] = section.title if section else 'No Section'
            # Ensure all fields are serializable
            for key, value in book_dict.items():
                if not isinstance(value, (str, int, float, bool, type(None))):
                    book_dict[key] = str(value)
            books_data.append(book_dict)
        print(f"Returning {len(books_data)} books: {books_data}")
        return jsonify(books_data), 200
    except Exception as e:
        print(f"Error fetching books: {str(e)}")
        return jsonify({'message': 'Error fetching books', 'error': str(e)}), 500

@app.route('/api/sections/<int:section_id>/books', methods=['GET'])
def get_section_books(section_id):
    try:
        books = Book.query.filter_by(section_id=section_id).all()
        books_data = [{
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'status': book.status,
            'description': book.description
        } for book in books]
        return jsonify(books_data), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching books', 'error': str(e)}), 500
    
    

@app.route('/test-books')
def test_books():
    try:
        books = Book.query.all()
        books_data = []
        for book in books:
            try:
                books_data.append(book.to_dict())
            except Exception as book_error:
                print(f"Error processing book {book.id}: {str(book_error)}")
        return jsonify({
            'message': f'Found {len(books)} books',
            'books': books_data
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error testing books: {str(e)}'}), 500
    
    

@app.route('/diagnose-books')
def diagnose_books():
    try:
        books = Book.query.all()
        diagnose_data = []
        for book in books:
            book_data = {
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'section_id': book.section_id,
                'status': book.status,
                'description': book.description
            }
            diagnose_data.append(book_data)
        return jsonify({
            'message': f'Found {len(books)} books',
            'books': diagnose_data
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error diagnosing books: {str(e)}'}), 500
    
    
# Route to update book request status (admin only)
@app.route('/api/book-requested/<int:request_id>', methods=['PATCH'])
def update_book_request(request_id):
    try:
        request_data = BookRequest.query.get_or_404(request_id)
        data = request.get_json()
        status = data.get('status')

        if status not in ['granted', 'rejected']:
            return jsonify({'message': 'Invalid status'}), 400

        request_data.status = status
        db.session.commit()
        return jsonify({'message': 'Request updated'}), 200
    except Exception as e:
        app.logger.error(f"Error in update_book_request: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'An error occurred ', 'error': str(e)}), 500

@app.route('/api/book-requests', methods=['GET'])
def get_book_requests():
    try:
        # Get the user_id from the query parameters
        user_id = request.args.get('user_id')
        
        if user_id:
            # If user_id is provided, filter requests for that user
            requests = BookRequest.query.filter_by(user_id=user_id).all()
        else:
            # If no user_id is provided, fetch all requests (you might want to restrict this for admin use)
            requests = BookRequest.query.all()
        
        requests_data = [{
            'id': req.id,
            'book_id': req.book_id,
            'book': {
                'name': req.book.name,
                'author': req.book.author
            },
            'user': {
                'id': req.user.id,
                'username': req.user.username
            },
            'status': req.status,
            'created_at': req.created_at.isoformat()
        } for req in requests]
        return jsonify(requests_data), 200
    except Exception as e:
        app.logger.error(f"Error fetching book requests: {str(e)}")
        return jsonify({'message': 'Error fetching book requests', 'error': str(e)}), 500    


@app.route('/api/test', methods=['GET'])
def test():
    try:
        return jsonify({"message": "CORS is working!"})
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
   
    
    
@app.route('/api/users/<username>', methods=['GET'])
def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first_or_404()
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'roles': [{'name': role.name} for role in user.roles] if user.roles else [{'name': 'No role assigned'}]
        }
        return jsonify(user_data), 200
    except Exception as e:
        app.logger.error(f"Error fetching user by username: {str(e)}")
        return jsonify({'message': 'Error fetching user details', 'error': str(e)}), 500
   
    

    
@app.route('/api/requested-books', methods=['GET'])
def get_requested_books():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    try:
        requests = BookRequest.query.filter_by(user_id=user_id).all()
        requested_books = [{'book_id': request.book_id, 'status': request.status} for request in requests]
        return jsonify(requested_books), 200
    except Exception as e:
        app.logger.error(f"Error fetching requested books: {str(e)}")
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.route('/api/RRbook-requests', methods=['POST'])
def create_book_requests():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        book_id = data.get('book_id')

        if not user_id or not book_id:
            return jsonify({'message': 'User ID and Book ID are required'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id, status='pending').first()
        if existing_request:
            return jsonify({'message': 'Request already exists', 'status': 'pending'}), 400

        new_request = BookRequest(user_id=user_id, book_id=book_id, status='pending')
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Request created', 'status': 'pending'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.get_or_404(user_id)
        book_requests = BookRequest.query.filter_by(user_id=user_id).all()
        
        requests_data = []
        for request in book_requests:
            book = Book.query.get(request.book_id)
            section = Section.query.get(book.section_id)
            requests_data.append({
                'id': request.id,
                'book_title': book.name,
                'section_title': section.title,
                'created_at': request.created_at.isoformat(),
                'days_requested': request.days_requested,
                'status': request.status
            })
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'requests': requests_data
        }
        return jsonify(user_data), 200
    except Exception as e:
        app.logger.error(f"Error fetching user by id: {str(e)}")
        return jsonify({'message': 'Error fetching user details', 'error': str(e)}), 500
    
@app.route('/api/book-requests/<int:request_id>', methods=['DELETE'])
def remove_book_request(request_id):
    try:
        book_request = BookRequest.query.get_or_404(request_id)
        db.session.delete(book_request)
        db.session.commit()
        return jsonify({'message': 'Book request removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error removing book request: {str(e)}")
        return jsonify({'message': 'An error occurred while removing the book request', 'error': str(e)}), 500
    
    
@app.route('/api/book-requests', methods=['POST'])
def create_new_book_request():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ('user_id', 'book_id')):
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Check if book exists and is available
        book = Book.query.get(data['book_id'])
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        if book.status != 'available':
            return jsonify({'message': 'Book is not available'}), 400

        # Create new book request
        new_request = BookRequest(
            user_id=data['user_id'],
            book_id=data['book_id'],
            days_requested=data.get('days_requested', 7),  # Default to 7 if not provided
            status='pending'
        )

        # Add and commit to database
        db.session.add(new_request)
        db.session.commit()

        # Prepare response
        response_data = {
            'message': 'Book request created successfully',
            'request_id': new_request.id,
            'user_id': new_request.user_id,
            'book_id': new_request.book_id,
            'status': new_request.status,
            'created_at': new_request.created_at.isoformat()
        }

        return jsonify(response_data), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating book request: {str(e)}")
        return jsonify({'message': 'An error occurred while processing your request'}), 500
    
    
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        # Book statistics
        pending_requests = BookRequest.query.filter_by(status='pending').count()
        books_issued = Book.query.filter_by(status='available').count()
        books_granted = BookRequest.query.filter_by(status='granted').count()
        books_rejected = BookRequest.query.filter_by(status='rejected').count()
        num_users = User.query.count()

        # Section statistics
        sections = Section.query.all()
        section_stats = {section.title: Book.query.filter_by(section_id=section.id).count() for section in sections}

        return jsonify({
            'bookStats': {
                'pendingRequests': pending_requests,
                'booksIssued': books_issued,
                'booksGranted': books_granted,
                'booksRejected': books_rejected,
                'numUsers': num_users
            },
            'sectionStats': section_stats
        }), 200
    except Exception as e:
        app.logger.error(f"Error fetching statistics: {str(e)}")
        return jsonify({'message': 'An error occurred while fetching statistics'}), 500
    
    
    
@app.route('/api/book-requested', methods=['POST'])
def create_book_request():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    days_requested = data.get('days_requested', 7)
    amount = data.get('amount', 0.0)

    if not user_id or not book_id:
        return jsonify({"error": "User ID and Book ID are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.is_blacklisted:
        return jsonify({"error": "User is blacklisted and cannot make requests"}), 403

    existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing_request:
        return jsonify({"error": "You have already requested this book"}), 400

    due_date = datetime.utcnow() + timedelta(days=days_requested)
    book_request = BookRequest(
        user_id=user_id,
        book_id=book_id,
        days_requested=days_requested,
        due_date=due_date
    )
    db.session.add(book_request)
    db.session.commit()

    return jsonify({"message": "Book request created successfully"}), 201

    
@app.route('/book_requested/<int:request_id>', methods=['GET'])
def get_book_request(request_id):
    book_request = BookRequest.query.get(request_id)
    if book_request:
        request_data = {
            'id': book_request.id,
            'user_id': book_request.user_id,
            'book_id': book_request.book_id,
            'status': book_request.status,
            'created_at': book_request.created_at,  # ISO format for JSON serialization
            'days_requested': book_request.days_requested,
            'due_date': book_request.due_date
        }
        return jsonify(request_data), 200
    else:
        return jsonify({"message": "BookRequest not found"}), 404
    
    
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Start a transaction
        db.session.begin_nested()

        # First, delete all related book requests
        BookRequest.query.filter_by(book_id=book_id).delete()

        # Then, delete the book
        book = Book.query.get(book_id)
        if book is None:
            db.session.rollback()
            return jsonify({"error": "Book not found"}), 404

        db.session.delete(book)

        # Commit the transaction
        db.session.commit()
        return jsonify({"message": "Book and related requests deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting book: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the book"}), 500
    

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error removing user: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while removing the user'}), 500

@app.route('/api/users/<int:user_id>/toggle-blacklist', methods=['POST'])
def toggle_user_blacklist(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user.is_blacklisted = not user.is_blacklisted
        db.session.commit()
        
        status = 'blacklisted' if user.is_blacklisted else 'whitelisted'
        return jsonify({'success': True, 'message': f'User {status} successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error toggling user blacklist: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while updating blacklist status'}), 500
    
    
@app.route('/api/users/<string:username>', methods=['PUT'])
def update_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if 'username' in data:
        new_username = data['username']
        if User.query.filter_by(username=new_username).first():
            return jsonify({'message': 'Username already exists'}), 400
        user.username = new_username

    if 'email' in data:
        user.email = data['email']

    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200



@app.route('/api/user-books', methods=['GET'])
def get_user_books():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        granted_requests = BookRequest.query.filter_by(user_id=user_id, status='granted').all()
        granted_book_ids = [request.book_id for request in granted_requests]

        books = Book.query.filter(Book.id.in_(granted_book_ids)).all()

        books_data = [{
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'description': book.description,
            'section': book.section.title if book.section else 'No Section',
            'status': book.status,
            'content': book.content[:20] + '...' if book.content else 'No content available',
            'rating': calculate_average_rating(book.id),
            'content_path': book.content
        } for book in books]
        
        return jsonify(books_data), 200
    except Exception as e:
        app.logger.error(f"Error fetching user books: {str(e)}")
        return jsonify({'message': 'Error fetching user books', 'error': str(e)}), 500
    
    
def calculate_average_rating(book_id):
    ratings = Rating.query.filter_by(book_id=book_id).all()
    if not ratings:
        return 0
    return sum(r.rating for r in ratings) / len(ratings)

@app.route('/api/download-book/<int:book_id>', methods=['GET'])
def download_book(book_id):
    try:
        # Retrieve the book from the database
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        # Get the content path from the book record
        content_path = book.content
        if not content_path:
            current_app.logger.error("No content path found for the book.")
            return jsonify({'message': 'No content path found for the book'}), 404

        # Define the base directory where the file should be saved
        base_dir = os.path.join(os.getcwd(), 'frontend', 'src', 'assets')

        # Ensure the directory exists
        os.makedirs(base_dir, exist_ok=True)

        # Full path where the file will be saved
        full_path = os.path.join(base_dir, content_path)

        # Check if the content already exists at the path, otherwise write it
        if not os.path.exists(full_path):
            with open(full_path, 'wb') as f:
                f.write(book.content.encode())  # Assuming the content is stored as a string

        return send_file(full_path, as_attachment=True, download_name=f"{book.name}.pdf")
    except Exception as e:
        current_app.logger.error(f"Error downloading book: {str(e)}")
        return jsonify({'message': 'Error downloading book', 'error': str(e)}), 500
    
    
@app.route('/api/return-book', methods=['POST'])
def return_book():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    if not user_id or not book_id:
        return jsonify({"error": "User ID and Book ID are required"}), 400

    book_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id, status='granted').first()
    if not book_request:
        return jsonify({"error": "No active request found for this book"}), 404

    book_request.status = 'returned'
    book = Book.query.get(book_id)
    book.status = 'available'

    db.session.commit()

    return jsonify({"message": "Book returned successfully"}), 200

    
    
@app.route('/api/statistics1', methods=['GET'])
def get_statisticss():
    try:
        # Book statistics
        pending_requests = BookRequest.query.filter_by(status='pending').count()
        books_granted = BookRequest.query.filter_by(status='granted').count()
        books_rejected = BookRequest.query.filter_by(status='rejected').count()
        books_returned = BookRequest.query.filter_by(status='returned').count()

        # Section statistics
        sections = Section.query.all()
        section_stats = {section.title: Book.query.filter_by(section_id=section.id).count() for section in sections}

        return jsonify({
            'bookStats': {
                'pendingRequests': pending_requests,
                'booksGranted': books_granted,
                'booksRejected': books_rejected,
                'booksReturned' : books_returned
            },
            'sectionStats': section_stats
        }), 200
    except Exception as e:
        app.logger.error(f"Error fetching statistics: {str(e)}")
        return jsonify({'message': 'An error occurred while fetching statistics'}), 500
    
    
    
    
# @app.route('/api/granted-books', methods=['GET'])
# def get_granted_books():
#     user_id = current_user.id  # Assuming user is logged in and current_user is available
#     granted_books = BookRequest.query.filter_by(user_id=user_id, status='granted').all()

#     books_data = []
#     for book_request in granted_books:
#         book = Book.query.get(book_request.book_id)
#         books_data.append({
#             'request_id': book_request.id,
#             'book_id': book.id,
#             'name': book.name,
#             'author': book.author,
#             'description': book.description,
#             'due_date': book_request.due_date
#         })

#     return jsonify(books_data)


@app.route('/api/rate-book', methods=['POST'])
def rate_book():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    rating_value = data.get('rating')
    feedback_text = data.get('feedback')

    # Create a new Rating entry
    rating = Rating(user_id=user_id, book_id=book_id, rating=rating_value)
    db.session.add(rating)
    db.session.commit()

    # Create a new Feedback entry linked to the rating
    feedback = Feedback(rating_id=rating.id, feedback=feedback_text)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Rating and feedback submitted successfully!'})


from flask import jsonify

@app.route('/api/user-bookss', methods=['GET'])
def get_myuser_books():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    books = Book.query.all()  # Assuming Book is your model for books
    book_list = []
    
    for book in books:
        ratings = Rating.query.filter_by(book_id=book.id).all()
        if ratings:
            avg_rating = sum(r.rating for r in ratings) / len(ratings)
        else:
            avg_rating = 0

        book_list.append({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'rating': avg_rating
        })
    
    return jsonify(book_list)

    