from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, post, comment

@app.route("/add/comment", methods = ["POST"])
def add_comment():
    data = {
        "comment":request.form["comment"],
        "user_id":session["user_id"],
        "post_id":request.form["post_id"]
    }
    comment.Comment.save_comment(data)
    return redirect(request.referrer)

