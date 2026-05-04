from flask import Blueprint, render_template, session, redirect, url_for
from database import db, Project, Task

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    # SQLAlchemy ORM queries
    total_projects   = Project.query.filter_by(user_id=user_id).count()
    total_tasks      = Task.query.filter_by(user_id=user_id).count()
    todo_tasks       = Task.query.filter_by(user_id=user_id, status='To-Do').count()
    inprogress_tasks = Task.query.filter_by(user_id=user_id, status='In Progress').count()
    done_tasks       = Task.query.filter_by(user_id=user_id, status='Done').count()

    recent_tasks = (
        Task.query
        .filter_by(user_id=user_id)
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template('dashboard.html',
        total_projects=total_projects,
        total_tasks=total_tasks,
        todo_tasks=todo_tasks,
        inprogress_tasks=inprogress_tasks,
        done_tasks=done_tasks,
        recent_tasks=recent_tasks
    )

