from datetime import datetime, timedelta
from flask import render_template, session, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask.ext.login import login_required, current_user
#from flask.ext.security import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm, \
                    ReservationForm, RoomForm, RoomsForm, BooksForm
from .. import db
from ..models import User, Role, Post, Permission, Comment, Room, Book
from app.decorators import admin_required, permission_required
from flask.ext.sqlalchemy import get_debug_queries
import os 
from app.main.forms import RoomBookingForm
from sqlalchemy.sql import and_
from flask.ext.social import Social

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if os.environ['BOOK_CONFIG'] == 'development' or query.duration >= current_app.config['BOOK_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning('Slow query: %s\n Parameters: %s\n Duration: %f\n Context: %s\n' %
                                       (query.statement, query.parameters, query.duration, query.context))
    return response

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    
    show_followed = False
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated():
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
        
    pagination = query.order_by(Post.timestamp.desc()).paginate(
                page, per_page=current_app.config['BOOK_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, 
                           show_followed=show_followed, pagination=pagination)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp
        
@main.route('/user/<email>')
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page,
                    per_page=current_app.config['BOOK_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)

    
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', email=current_user.email))
    
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', email=user.email))
    
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    
    page = request.args.get('page', 1, type=int)
    if page == -1:            # give the server a second to ensure it is up
        page = (post.comments.count() - 1) / current_app.config['BOOK_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page,
                    per_page=current_app.config['BOOK_COMMENTS_PER_PAGE'], error_out=False) 
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)

@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id) 
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
        
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data 
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/follow/<email>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', email=email))
    
    current_user.follow(user)
    flash('You are now following %s.' % email)
    return redirect(url_for('.user', email=email))

@main.route('/unfollow/<email>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', email=email))
    
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % email)
    return redirect(url_for('.user', email=email))

@main.route('/followers/<email>')
def followers(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page,
                                         per_page=current_app.config['BOOK_FOLLOWERS_PER_PAGE'],
                                         error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Followers of',
                           endpoint='.followers', pagination=pagination, follows=follows)
    
@main.route('/followed_by/<email>')  
def followed_by(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, 
                                        per_page=current_app.config['BOOK_FOLLOWERS_PER_PAGE'],
                                        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Followed by',
                           endpoint='.followed_by', pagination=pagination, follows=follows)

    
@main.route('/moderate-comments')
@login_required
@permission_required(Permission.MODERATE_COMMENTS) 
def moderate_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, 
                    per_page=current_app.config['BOOK_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('moderate_comments.html', comments=comments, pagination=pagination, page=page)

@main.route('/moderate_comments/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate_comments', page=request.args.get('page', 1, type=int)))

@main.route('/moderate_comments/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate_comments', page=request.args.get('page', 1, type=int)))
  
@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Sutting down...'

@main.route('/reservation', methods=['GET', 'POST'])
@login_required
@admin_required
def reservation():
    form = ReservationForm()
    booking_form = RoomBookingForm()
    from_date = None
    to_date = None
    min_date = None
    max_date = None
    rooms = []
    rooms_schedules = []
    pagination = []
    interval = 15
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        min_date = from_date - timedelta(days=interval)
        max_date = from_date + timedelta(days=interval)
    else:
        booking_form.email.data = request.args.get('email')
        booking_form.name.data = request.args.get('name')
        booking_form.mobile.data = request.args.get('mobile')
        booking_form.phone.data = request.args.get('phone')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        if to_date:
            form.to_date.data = to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        if from_date:
            form.from_date.data = from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        else:
            form.from_date.data = from_date = datetime.today().date()
        print('>> from_date: %s ' % from_date)   
        min_date = from_date - timedelta(days=interval)
        max_date = from_date + timedelta(days=interval)

    if from_date and to_date:    
        pagination = Book.available_rooms(from_date, to_date)\
            .paginate(page=page, per_page=per_page, error_out=False)
        rooms = pagination.items
        entries = Book.rooms_schedules(rooms, from_date=min_date, to_date=max_date)
        rooms_schedules = [{"number": r.number, "name": r.name.encode('utf-8'), "id": b.id, 
                           "checkin_on": str(b.checkin_on), "checkout_on": str(b.checkout_on),
                           "room_count": b.room_count, "user": b.user.to_json()} for (r, b) in entries]
        
    return render_template('reservation.html', rooms=rooms, rooms_schedules=rooms_schedules, from_date=from_date, to_date=to_date,
                           min_date=min_date, max_date=max_date, page=page, pagination=pagination, booking_form=booking_form, form=form)

@main.route('/reservation/booking', methods=['GET', 'POST'])
@login_required
@admin_required
def booking():
    form = ReservationForm()
    booking_form = RoomBookingForm()
    if booking_form.validate_on_submit():
        from_date = booking_form.from_date.data
        to_date = booking_form.to_date.data
        email = booking_form.email.data
        name = booking_form.name.data
        mobile = booking_form.mobile.data
        phone = booking_form.phone.data
        room_ids = request.form.getlist('room_id', type=int)
        
        #print('>> form.booking: %s \n' % room_ids)
        if room_ids and Book.available_booking(room_ids, from_date, to_date):
            book = Book(checkin_on=from_date, checkout_on=to_date, room_count=len(room_ids), 
                        email=email, name=name, mobile=mobile,phone=phone)
            for id in room_ids:
                room = Room.query.get_or_404(id)
                book.rooms.append(room)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('.book', id=book.id))
        else:
            if not room_ids:
                flash("You should select Rooms.")
            else:
                flash("Selected rooms are already reserved.")
    #print('>>> booking_form.from_date: %s' % booking_form.from_date)
    form.from_date = booking_form.from_date
    form.to_date = booking_form.to_date
    return render_template('reservation.html', form=form, booking_form=booking_form, page=request.args.get('page', 1, type=int))

@main.route('/book/<int:id>')
@login_required
@admin_required
def book(id):
    book = Book.query.get_or_404(id)
    #print('>> book: %s' % book.to_json())
    rooms_schedule = []
    from_date = None
    to_date = None
    if book:
        #book.rooms
        #book.user
        from_date = book.checkin_on - timedelta(days=15)
        to_date = book.checkin_on + timedelta(days=15)
        entries = book.rooms_schedule()
        rooms_schedule = [{"number": r.number, "name": r.name.encode('utf-8'), "id": b.id, 
                           "checkin_on": str(b.checkin_on), "checkout_on": str(b.checkout_on),
                           "room_count": b.room_count, "user": b.user.to_json()} for (r, b) in entries]
    
    #print('>> book2: %s' % book.to_json())
    return render_template('book.html', book=book, rooms_schedule=rooms_schedule, from_date=from_date, to_date=to_date)

@main.route('/books', methods=['GET', 'POST'])
@login_required
@admin_required
def books():
    form = BooksForm()
    name = None  
    email = None 
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        name = form.name.data
        email= form.email.data
    else:
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        name = request.args.get('name')
        email = request.args.get('email')
        if from_date:
            form.from_date.data = datetime.strptime(from_date, '%Y-%m-%d')
        if to_date:
            form.to_date.data = datetime.strptime(to_date, '%Y-%m-%d')
        if name:
            form.name.data = name
        if email:
            form.email.data = email
            
    page = request.args.get('page', 1, type=int)   
    print('>>name:  %s' % name) 
    #build query
    filters = []
    if from_date:
        filters.append(Book.checkin_on >= from_date)
    if to_date:
        filters.append(Book.checkin_on <= to_date)
    if name:
        filters.append(Book.user_id == User.query.with_entities(User.id).filter_by(name=name))
    if email:
        filters.append(Book.user_id == User.query.with_entities(User.id).filter_by(email=email))
    pagination = Book.query.filter(and_(*filters)).order_by(Book.checkin_on.desc()).paginate(page=page, error_out=False)
    books = pagination.items
    return render_template('books.html', books=books, pagination=pagination, from_date=from_date, to_date=to_date,
                           name=name, email=email, form=form)
    
@main.route('/room/<int:number>', methods=['GET', 'POST'])
@login_required
@admin_required
def room(number):
    form = RoomForm()
    from_date = datetime.today().date()
    to_date = from_date + timedelta(days=30)
    if form.from_date.data is None:
        form.from_date.data = from_date
        form.to_date.data = to_date
    room = Room.query.filter_by(number=number).first()
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        
    books = room.between_books(from_date, to_date)
    json_books = [book.to_json() for book in books]
    
    return render_template('room.html', room=room, books=json_books, form=form)

@main.route('/room/<int:number>/edit', methods=['GET','POST'])
@login_required
@admin_required
def edit_room(number):
    form = RoomsForm()
    room = Room.query.filter_by(number=number).first()
    if room:
        form.number.data = room.number
        form.name.data = room.name
        form.guests.data = room.guests
        form.active.data = room.active
    return render_template('edit_room.html', room=room, form=form)

@main.route('/room/<int:number>/update', methods=['POST'])
@login_required
@admin_required
def update_room(number):
    form = RoomsForm()
    page = request.args.get('page', 1, type=int)
    room = Room.query.filter_by(number=number).first()
    if room and form.validate_on_submit():
        room.number = form.number.data 
        room.name = form.name.data 
        room.guests = form.guests.data 
        room.active = form.active.data 
        try:
            db.session.commit()
        except Exception as e:
            #print(str(e.args[0]))
            flash(e.message)
            db.session.rollback()
            return render_template('edit_room.html', room=room, form=form)
        return redirect(url_for('.rooms', page=page))
    return render_template('edit_room.html', room=room, form=form)
        
@main.route('/rooms', methods=['GET', 'POST'])
@login_required
@admin_required
def rooms():
    form = RoomsForm()
    if form.validate_on_submit():
        room = Room()
        room.number = form.number.data
        room.name = form.name.data
        room.guests = form.guests.data
        room.active = form.active.data
        
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('.rooms', page=request.args.get('page', 1, type=int)))
    page = request.args.get('page', 1, type=int)    
    pagination = Room.query.order_by(Room.number.asc()).paginate(page=page, error_out=False)
    rooms = pagination.items

    rooms_schedules = []
    from_date = None
    to_date = None
    if rooms:
        from_date = datetime.today().date() - timedelta(days=15)
        to_date = datetime.today().date() + timedelta(days=15)
        entries = Book.rooms_schedules(rooms)
        rooms_schedules = [{"number": r.number, "name": r.name.encode('utf-8'), "id": b.id, 
                           "checkin_on": str(b.checkin_on), "checkout_on": str(b.checkout_on),
                           "room_count": b.room_count, "user": b.user.to_json()} for (r, b) in entries]

    return render_template('rooms.html', rooms=rooms, pagination=pagination, rooms_schedules=rooms_schedules,
                           from_date=from_date, to_date=to_date, form=form)

