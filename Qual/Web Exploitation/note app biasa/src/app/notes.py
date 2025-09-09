from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Note
from .auth import login_required
from . import db


notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    return render_template('notes/dashboard.html', notes=notes)

@notes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return render_template('notes/create.html')
        
        note = Note(
            title=title,
            content=content,
            user_id=session['user_id']
        )
        db.session.add(note)
        db.session.commit()

        # redirect to the note
        
        flash('Note created successfully!', 'success')
        return redirect('/notes/view/' + note.id)
    
    return render_template('notes/create.html')

@notes_bp.route('/edit/<string:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    # Check if user owns this note
    if note.user_id != session['user_id']:
        flash('You can only edit your own notes!', 'error')
        return redirect(url_for('notes.dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return render_template('notes/edit.html', note=note)
        
        note.title = title
        note.content = content
        db.session.commit()
        
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.dashboard'))
    
    return render_template('notes/edit.html', note=note)

@notes_bp.route('/view/<string:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    return render_template('notes/view.html', note=note)

@notes_bp.route('/delete/<string:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if session.get('is_admin') or note.user_id == session['user_id']:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted successfully!', 'success')
    else:
        flash('You can only delete your own notes!', 'error')
    return redirect(url_for('notes.dashboard'))
