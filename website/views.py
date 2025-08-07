from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/my-notes/", methods=["GET", "POST"])
@login_required
def my_notes():
    if request.method == "POST":
        if "note" in request.form:
            note_data = request.form.get("note")
            if len(note_data) < 1:
                flash("Note cannot be empty.", "error")
            elif len(note_data) > 10000:
                flash("Note length needs to be less than 10000 characters", "error")
            else:
                new_note = Note(data=note_data, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash("Note has been added.", "success")
        elif "note_id" in request.form:
            note_id = request.form.get("note_id")
            note = Note.query.get(note_id)
            if note and note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
                flash("Note deleted.", "success")
        else:
            flash("Invalid POST request.", "error")
        
    return render_template("my_notes.html", user=current_user)

@views.route("/delete-note", methods=["GET", "POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["note_id"]
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return "True"
