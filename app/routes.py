from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import User, Event, Category, EventAttendees
from app import db

main = Blueprint('main', __name__)

### AUTHENTICATION ROUTES ###

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists!')
            
        new_user = User(username=username, role=role)
        db.session.add(new_user)
        db.session.commit() 

        return render_template('register.html', success=f'{role} : {username} registered successfully!')

    return render_template('register.html')

@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        return redirect(url_for('main.index', error='User does not exist!'))

    session['user_id'] = user.id  
    session['username'] = user.username 
    session['role'] = user.role

    if user.role == 'user':
        return redirect(url_for('main.user_dashboard'))
    elif user.role == 'producer':
        return redirect(url_for('main.producer_dashboard'))

### PRODUCER ROUTES ###

@main.route('/producer/dashboard')
def producer_dashboard():
    producer_id = session.get('user_id')
    events = Event.query.filter_by(producer_id=producer_id).all()
    event_attendance_counts = {}
    for event in events:
        attendee_count = EventAttendees.query.filter_by(event_id=event.id).count()
        event_attendance_counts[event.id] = attendee_count

    return render_template('producer_dashboard.html', events=events, event_attendance_counts=event_attendance_counts)


@main.route('/producer/event/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        category_id = request.form.get('category_id')
        producer_id = session.get('user_id')

        new_event = Event(name=name, date=date, category_id=category_id, producer_id=producer_id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.producer_dashboard'))

    categories = Category.query.all()
    return render_template('create_event.html', categories=categories)

@main.route('/producer/event/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        event.name = request.form.get('name')
        event.date = request.form.get('date')
        event.category_id = request.form.get('category_id')
        db.session.commit()
        return redirect(url_for('main.producer_dashboard'))

    categories = Category.query.all()
    return render_template('edit_event.html', event=event, categories=categories)

@main.route('/producer/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('main.producer_dashboard'))

@main.route('/category/create', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        name = request.form.get('name')

        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            return render_template('create_category.html', error='Category already exists!')

        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('main.create_category'))

    return render_template('create_category.html')

### USER ROUTES ###

@main.route('/user/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    user_id = session.get('user_id')
    categories = Category.query.all()

    category_id = request.args.get('category_id')
    if category_id:
        events = Event.query.filter_by(category_id=category_id).order_by(Event.date.desc()).all()
    else:
        events = Event.query.order_by(Event.date.desc()).all()

    attending_events = EventAttendees.query.filter_by(user_id=user_id).all()
    attending_event_ids = {attendance.event_id for attendance in attending_events}

    return render_template('user_dashboard.html', events=events, categories=categories, attending_event_ids=attending_event_ids)

@main.route('/event/<int:event_id>/attend', methods=['POST'])
def attend_event(event_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))

    existing_attendance = EventAttendees.query.filter_by(event_id=event_id, user_id=user_id).first()
    
    if existing_attendance:
        return redirect(url_for('main.user_dashboard'))
    else:
        new_attendance = EventAttendees(event_id=event_id, user_id=user_id)
        db.session.add(new_attendance)
        db.session.commit()

    return redirect(url_for('main.user_dashboard'))

@main.route('/event/<int:event_id>/remove', methods=['POST'])
def remove_attendance(event_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.index'))

    attendance = EventAttendees.query.filter_by(event_id=event_id, user_id=user_id).first()
    
    if attendance:
        db.session.delete(attendance)
        db.session.commit()

    return redirect(url_for('main.user_dashboard'))
