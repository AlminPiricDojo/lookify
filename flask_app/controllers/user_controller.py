from flask import Flask, render_template
from flask_app import app
from flask_app.models.user_model import User

@app.route("/users/<int:id>")
def show_user(id):
    user = User.get_user_songs(id)
    return render_template("view_user.html", user=user)