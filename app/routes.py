from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Note
from . import db, login_manager

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        return 'User already exists'
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return 'Registered successfully'

@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return 'Logged in successfully'
    return 'Invalid credentials'

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

@main.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        content = request.json.get('content')
        note = Note(content=content, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        return jsonify({'message': 'Note added'})
    else:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        return jsonify([{'id': n.id, 'content': n.content} for n in notes])

@main.route('/notes/<int:note_id>', methods=['PUT', 'DELETE'])
@login_required
def modify_note(note_id):
    note = Note.query.get(note_id)
    if note.user_id != current_user.id:
        return 'Unauthorized', 403

    if request.method == 'PUT':
        note.content = request.json.get('content')
        db.session.commit()
        return jsonify({'message': 'Note updated'})
    elif request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted'})
