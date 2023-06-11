# -*- coding: utf-8 -*-
from datetime import datetime

from flask import current_app
from flask import flash
from flask import g
from flask import jsonify
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_babel import _
from flask_login import current_user
from flask_login import login_required
from guess_language import guess_language

from app import db
from app.main import bp
from app.main.forms import EditProfileForm
from app.main.forms import EmptyForm
from app.main.forms import MessageForm
from app.main.forms import PostForm
from app.main.forms import SearchForm
from app.models import Message
from app.models import Notification
from app.models import Post
from app.models import User
from app.translate import translate


UNKNOWN_LANGUAGE = 'UNKNOWN'
UNREAD_MSG_COUNT_NOTIF = 'unread_message_count'
MAX_LANGUAGE_LEN = 10


@bp.before_request
def before_request():
    """Before request executions."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route("/admin/reindex")
@login_required
def reindex():
    Post.reindex()
    flash(_("Reindex done."))
    return redirect(url_for("main.index"))


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post_body = form.post.data
        language = guess_language(post_body)
        if language == UNKNOWN_LANGUAGE or len(language) > 10:
            language = ""
        post = Post(body=post_body, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_("Your post is now live!"))
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    posts_paginator = current_user.followed_posts().paginate(
        page=page,
        max_per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False,
    )
    next_page_url = (
        url_for("main.index", page=posts_paginator.next_num)
        if posts_paginator.has_next
        else None
    )
    prev_page_url = (
        url_for("main.index", page=posts_paginator.prev_num)
        if posts_paginator.has_prev
        else None
    )
    posts = posts_paginator.items
    return render_template(
        "index.html",
        title="Home",
        form=form,
        posts=posts,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        new_page_title="Older posts",
        prev_page_title="Newer posts",
    )


@bp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    posts_paginator = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        max_per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False,
    )
    next_page_url = (
        url_for("main.explore", page=posts_paginator.next_num)
        if posts_paginator.has_next
        else None
    )
    prev_page_url = (
        url_for("main.explore", page=posts_paginator.prev_num)
        if posts_paginator.has_prev
        else None
    )
    posts = posts_paginator.items
    return render_template(
        "index.html",
        title="Explore",
        posts=posts,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        new_page_title="Older posts",
        prev_page_title="Newer posts",
    )


@bp.route("/user/<username>")
@login_required
def user(username):
    user_instance = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts_paginator = user_instance.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,
        max_per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False,
    )
    next_page_url = (
        url_for("main.user", username=username, page=posts_paginator.next_num)
        if posts_paginator.has_next
        else None
    )
    prev_page_url = (
        url_for("main.user", username=username, page=posts_paginator.prev_num)
        if posts_paginator.has_prev
        else None
    )
    posts = posts_paginator.items
    form = EmptyForm()
    return render_template(
        "user.html",
        user=user_instance,
        posts=posts,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        form=form,
    )


@bp.route("/user/<username>/popup")
@login_required
def user_popup(username):
    user_instance = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user_instance)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@bp.route("/follow/<username>", methods=["GET", "POST"])
@login_required
def follow(username):
    user_instance = User.query.filter_by(username=username).first()
    if user_instance is None:
        flash(_("User %(username)s not found", username=username))
        return redirect(url_for("main.index"))
    if user_instance == current_user:
        flash("You can't follow yourself!")
        return redirect(url_for("main.user", username=username))
    current_user.follow(user_instance)
    db.session.commit()
    flash(f"You're now following {username}")
    return redirect(url_for("main.user", username=username))


@bp.route("/unfollow/<username>", methods=["GET", "POST"])
@login_required
def unfollow(username):
    user_instance = User.query.filter_by(username=username).first()
    if user_instance is None:
        flash(f"User {username} not found")
        return redirect(url_for("main.index"))
    if user_instance == current_user:
        flash("You can't unfollow yourself!")
        return redirect(url_for("main.user", username=username))
    current_user.unfollow(user_instance)
    db.session.commit()
    flash(f"You don't follow {username} anymore.")
    return redirect(url_for("main.user", username=username))


@bp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    return jsonify(
        {
            "text": translate(
                request.form["text"],
                request.form["source_language"],
                request.form["dest_language"],
            )
        }
    )


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    max_posts = current_app.config['POSTS_PER_PAGE']
    posts, total = Post.search(g.search_form.q.data, page, max_posts)
    next_page_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * max_posts else None
    prev_page_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template(
        'search.html', title=_('Search'), posts=posts, 
        next_url=next_page_url, prev_url=prev_page_url
    )


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user_instance = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            author=current_user,
            recipient=user_instance,
            body=form.message.data,
        )
        db.session.add(msg)
        user_instance.add_notification(
            UNREAD_MSG_COUNT_NOTIF,
            user_instance.new_messages_count(),
        )
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template(
        'send_message.html',
        title=_('Send Message'),
        form=form,
        recipient=recipient,
    )


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification(UNREAD_MSG_COUNT_NOTIF, 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages_paginator = current_user.messages_received.order_by(
        Message.timestamp.desc()
    ).paginate(
        page=page,
        max_per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False,
    )
    next_page_url = (
        url_for("main.messages", page=messages_paginator.next_num)
        if messages_paginator.has_next else None
    )
    prev_page_url = (
        url_for("main.messages", page=messages_paginator.prev_num)
        if messages_paginator.has_prev else None
    )
    messages_list = messages_paginator.items
    return render_template(
        "messages.html",
        messages=messages_list,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
    )


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifs = current_user.notifications.filter(
        Notification.timestamp > since
    ).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': notification.name,
        'data': notification.get_data(),
        'timestamp': notification.timestamp,
    } for notification in notifs])


@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_posts', _('Exporting posts.'))
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))
