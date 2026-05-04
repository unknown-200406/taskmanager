from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db, Project, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/projects/<int:project_id>/tasks')
def tasks(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.filter_by(
        id=project_id, user_id=session['user_id']
    ).first_or_404()

    status_filter   = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')

    # Build query dynamically using ORM
    query = Task.query.filter_by(project_id=project_id, user_id=session['user_id'])

    if status_filter:
        query = query.filter(Task.status == status_filter)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)

    all_tasks = query.order_by(Task.created_at.desc()).all()

    return render_template('tasks.html',
        project=project,
        tasks=all_tasks,
        status_filter=status_filter,
        priority_filter=priority_filter
    )

@tasks_bp.route('/projects/<int:project_id>/tasks/add', methods=['POST'])
def add_task(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title       = request.form['title'].strip()
    description = request.form.get('description', '').strip()
    priority    = request.form.get('priority', 'Medium')
    due_date_str = request.form.get('due_date', '')

    if not title:
        flash('Task title is required.', 'danger')
        return redirect(url_for('tasks.tasks', project_id=project_id))

    # Parse due_date string to Python date object
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            due_date = None

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        project_id=project_id,
        user_id=session['user_id']
    )
    db.session.add(new_task)
    db.session.commit()

    flash('Task added successfully!', 'success')
    return redirect(url_for('tasks.tasks', project_id=project_id))

@tasks_bp.route('/tasks/update-status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    new_status = request.form['status']
    project_id = request.form['project_id']

    task = Task.query.filter_by(
        id=task_id, user_id=session['user_id']
    ).first_or_404()

    task.status = new_status       # ORM attribute update
    db.session.commit()

    flash('Task status updated!', 'success')
    return redirect(url_for('tasks.tasks', project_id=project_id))

@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    project_id = request.form['project_id']

    task = Task.query.filter_by(
        id=task_id, user_id=session['user_id']
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash('Task deleted.', 'warning')
    return redirect(url_for('tasks.tasks', project_id=project_id))

