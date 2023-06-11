import json
import sys
import time

from flask import render_template
from rq import get_current_job

from app import constants
from app import create_app
from app import db
from app.email import send_email
from app.models import Post
from app.models import Task
from app.models import User


app = create_app()
app.app_context().push()


def _set_task_progress(progress: int) -> None:
    """Set progress percentage to Task object."""
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification(
            constants.TASK_PROGRESS_NOTIF,
            {
                'task_id': job.get_id(),
                'progress': progress,
            }
        )
        app.logger.info(f'Completeness percentage: {progress}')

        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id: int) -> None:
    """Export all user posts to JSON and send mail result."""
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        total_posts = user.posts.count()
        for i, post in enumerate(
                user.posts.order_by(Post.timestamp.asc()),
                start=1
        ):
            data.append({
                'body': post.body,
                'timestamp': f'{post.timestamp.isoformat()}Z',
            })
            time.sleep(3)
            _set_task_progress(100 * i // total_posts)

        send_email(
            '[Microblog] Your blog posts',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/export_posts.txt', user=user),
            html_body=render_template('email/export_posts.html', user=user),
            attachments=[(
                'posts.json',
                'application/json',
                json.dumps({'posts': data}, indent=4)
            )],
            send_async=False,
        )
        app.logger.info('Result mail send successfully.')
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
