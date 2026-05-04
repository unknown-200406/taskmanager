from flask import Flask,redirect, url_for
from database import db
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.tasks import tasks_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

# ── Config ────────────────────────────────────────────
app.secret_key = 'your_secret_key_here_change_in_production'

# ✅ MySQL Connection — change these values to match your MySQL Workbench setup
MYSQL_USER     = 'root'           # your MySQL username
MYSQL_PASSWORD = '1234'  # your MySQL password
MYSQL_HOST     = 'localhost'      # or 127.0.0.1
MYSQL_PORT     = '3306'           # default MySQL port
MYSQL_DB       = 'taskflow_db'    # database name (create this in Workbench first)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── Init SQLAlchemy ───────────────────────────────────
db.init_app(app)

# ── Register Blueprints ───────────────────────────────
app.register_blueprint(auth_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(dashboard_bp)

# ── Create Tables ─────────────────────────────────────
with app.app_context():
    db.create_all()
    print("✅ MySQL tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
