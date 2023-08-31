from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_app.models.song_model import Song

from flask_app.models import user_model

@app.route("/")
def index():
    users = user_model.User.get_all() # NEW
    songs = Song.get_all()
    return render_template("index.html", users=users, songs=songs) # Pass users to index.html

@app.route("/songs/add", methods=['GET', 'POST'])
def add_song():
    if request.method == 'GET':
        users = user_model.User.get_all()
        return render_template("add_song.html", users=users)
    
    data = {
        'title': request.form['title'],
        'artist': request.form['artist'],
        'rating': request.form['rating'],
        'user_id': request.form['user_id']
    }
    Song.save(data)

    return redirect("/")

@app.route("/songs/<int:id>")
def show_song(id):
    song = Song.get_one(id)
    return render_template("show_song.html", song=song)

@app.route("/songs/<int:id>/update", methods=['GET', 'POST'])
def update_song(id):
    if request.method == 'GET':
        song = Song.get_one(id)
        users = user_model.User.get_all()
        return render_template("update_song.html", song=song, users=users)
    
    data = {
        'id': id,
        'title': request.form['title'],
        'artist': request.form['artist'],
        'rating': request.form['rating'],
        'user_id': request.form['user_id']
    }
    song = Song.update(data)
    return redirect("/")

@app.route("/songs/<int:id>/delete")
def delete_song(id):
    Song.delete(id)
    return redirect("/")