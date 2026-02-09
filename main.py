from flask import Flask, render_template
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

# Регистрация blueprints
from routes.tasks import tasks_bp
from routes.tags import tags_bp
from routes.dashboard import dashboard_bp
from routes.export import export_bp
from routes.done import done_bp
from routes.import_tasks import import_bp
from routes.rice import rice_bp
from routes.users import users_bp
from routes.groups import groups_bp

app.register_blueprint(tasks_bp)
app.register_blueprint(tags_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(export_bp)
app.register_blueprint(done_bp)
app.register_blueprint(import_bp)
app.register_blueprint(rice_bp)
app.register_blueprint(users_bp)
app.register_blueprint(groups_bp)


# Маршруты для страниц
@app.route('/')
def index():
    return render_template('kanban.html')


@app.route('/kanban')
def kanban():
    return render_template('kanban.html')


@app.route('/rice')
def rice():
    return render_template('rice.html')


@app.route('/rice/kanban')
def rice_kanban():
    return render_template('rice_kanban.html')


@app.route('/rice/ideas')
def rice_ideas():
    return render_template('rice_ideas.html')


@app.route('/eisenhower')
def eisenhower():
    return render_template('eisenhower.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/done')
def done():
    return render_template('done.html')


@app.route('/group/<int:group_id>')
def group_view(group_id):
    """Просмотр задач группы"""
    return render_template('group.html', group_id=group_id)


# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
