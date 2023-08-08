from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Post, User, Comment, Like
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html", user=current_user)


@views.route('/makepost', methods=['GET', 'POST'])
@login_required
def make_post():
    if request.method == 'POST':
        post = request.form.get('post')
        if not post:
            flash("Post cannot be empty.", category='error')
        else:
            new_post = Post(post=post, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created!", category='success')
            return redirect(url_for('views.forum'))

    return render_template("makepost.html", user=current_user)


@views.route('/mynotes', methods=['GET', 'POST'])
@login_required
def my_notes():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note:
            flash("Note cannot be empty.", category='error')
        else:
            new_note = Note(post=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')

    return render_template("mynotes.html", user=current_user)


@views.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    posts = Post.query.all()
    if request.method == 'POST':
        pass
    
    return render_template("forum.html", user=current_user, posts=posts)


@views.route("/post/<first_name>", methods=['GET', 'POST'])
@login_required
def view_posts(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    
    if not user:
        flash('No such user exists', category='error')
        return redirect(url_for('views.forum'))
    
    posts = user.posts
    return render_template("viewposts.html", user=current_user, posts=posts, author=first_name)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note.get('noteId')
    print(note)
    if noteId is not None:
        note = Note.query.get(noteId)
        if note and note.user_id == current_user.id:
            print('deleting note: ', note)
            db.session.delete(note)
            db.session.commit()
            print('Note deleted')
            return jsonify({'message': 'Note deleted successfully.'})
    return jsonify({'message': 'Not authorized to delete note.'})


@views.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
    post = json.loads(request.data)
    postId = post.get('postId')
    print(post)
    if postId is not None:
        post = Post.query.get(postId)
        if post and post.user_id == current_user.id:
            print('deleting post: ', post)
            db.session.delete(post)
            db.session.commit()
            print('Post deleted')
            return jsonify({'message': 'Post deleted successfully.'})
    return jsonify({'message': 'Not authorized to delete note.'})


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    
    if not text:
        flash('Comment cannot be empty.', category='error')
    post = Post.query.filter_by(id=post_id)
    if post:
        comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
    else:
        flash('Post does not exist.', category='error')
    
    return redirect(url_for('views.forum'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.user_id:
        flash('You are not authorized.')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.forum'))


@views.route("/like-post/<post_id>",  methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        print('liked')
    
    return jsonify({"likes": len(post.likes), "liked": any(like.user_id == current_user.id for like in post.likes)})

   










