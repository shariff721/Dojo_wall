from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, post


@app.route("/process/post", methods = ["POST"])
def add_post():
    if not post.Post.validate_post(request.form):
        return redirect(request.referrer)
    data = {
        "content":request.form["content"],
        "user_id":session["user_id"]
    }
    post_id = post.Post.save_post(data)
    session['post_id'] = post_id
    return redirect(request.referrer)

@app.route("/delete/post/<int:id>")
def remove_post(id):
    data = {
        "id":id
    }
    post.Post.delete_post(data)
    return redirect("/dashboard")


