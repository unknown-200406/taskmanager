from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db, Project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects')
def projects():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    all_projects = (
        Project.query
        .filter_by(user_id=session['user_id'])
        .order_by(Project.created_at.desc())
        .all()
    )
    return render_template('projects.html', projects=all_projects)

@projects_bp.route('/projects/add', methods=['POST'])
def add_project():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title       = request.form['title'].strip()
    description = request.form.get('description', '').strip()

    if not title:
        flash('Project title is required.', 'danger')
        return redirect(url_for('projects.projects'))

    new_project = Project(
        title=title,
        description=description,
        user_id=session['user_id']
    )
    db.session.add(new_project)
    db.session.commit()

    flash('Project created successfully!', 'success')
    return redirect(url_for('projects.projects'))

@projects_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.filter_by(
        id=project_id, user_id=session['user_id']
    ).first_or_404()

    db.session.delete(project)   # cascade deletes tasks too
    db.session.commit()

    flash('Project deleted.', 'warning')
    return redirect(url_for('projects.projects'))

