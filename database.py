from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Single shared db instance - imported everywhere
db = SQLAlchemy()

# ── Models ────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    projects = db.relationship('Project', backref='owner', lazy=True,
                            cascade='all, delete-orphan')
    tasks    = db.relationship('Task', backref='owner', lazy=True,
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship
    tasks = db.relationship('Task', backref='project', lazy=True,
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.title}>'


class Task(db.Model):
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    status      = db.Column(db.String(20), default='To-Do')     # To-Do / In Progress / Done
    priority    = db.Column(db.String(10), default='Medium')    # High / Medium / Low
    due_date    = db.Column(db.Date, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

