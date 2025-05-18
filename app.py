import json
from flask_login import LoginManager, login_required, login_user, logout_user
import add_job
from data.jobs import Jobs
from data import db_session
import os
import random
from flask import Blueprint, Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from data.users import User
import auth

CAROUSEL_FOLDER = os.path.join(os.path.dirname(
    __file__), 'static', 'img', 'carousel')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DB_PATH = os.path.join(os.path.dirname(__file__), 'mars.db')

bp = Blueprint('main', __name__)
login_manager = LoginManager()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id: int):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@bp.route("/training/<prof>")
@login_required
def training(prof: str):
    prof = prof.lower()
    if "инженер" in prof or "строитель" in prof:
        tr = "Инженерные тренажеры"
        image = url_for("static", filename="img/engineer.jpg")
    else:
        tr = "Научные симуляторы"
        image = url_for("static", filename="img/simulators.jpg")
    return render_template("training.html", training=tr, image=image)


@bp.route("/list_prof/<list_type>")
@login_required
def list_prof(list_type: str):
    if list_type in ("ol", "ul"):
        return render_template("list_prof.html", list_type=list_type)
    else:
        return render_template("error.html", error="Неизвестный тип списка")


@bp.route("/answer")
@bp.route("/auto_answer")
@login_required
def auto_answer():
    param = {
        "surname": "Watny",
        "name": "Mark",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "male",
        "motivation": "Всегда мечтал застрять на Марсе!",
        "ready": str(True),
        "title": "Анкета"
    }

    return render_template("auto_answer.html", **param)


@bp.route("/distribution")
@login_required
def distribution():
    crew = [
        "Ридли Скотт",
        "Энди Уир",
        "Марка Уотни",
        "Венката Капур",
        "Тедди Сандерс",
        "Шон Бин"
    ]
    return render_template("distribution.html", astronauts=crew)


@bp.route("/table/<gender>/<int:age>")
@login_required
def cabin_decor(gender: str, age: int):
    if gender == "female":
        wall_color = "#FFA07A" if age < 21 else "#FF4500"
    else:
        wall_color = "#B0C4DE" if age < 21 else "#007FF0"

    alien_image = "alien_young.png" if age < 21 else "alien_old.png"

    return render_template("table.html",
                           wall_color=wall_color,
                           alien_image=alien_image)


@bp.route("/member")
@login_required
def show_member():
    with open("templates/crew.json", encoding="utf-8") as f:
        crew = json.load(f)
    member = random.choice(crew)
    return render_template("member.html", member=member)


@bp.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(CAROUSEL_FOLDER, filename))
        return redirect(url_for('gallery'))
    images = sorted(os.listdir(CAROUSEL_FOLDER))
    return render_template('gallery.html', images=images)


@bp.route('/')
def index():
    session = db_session.create_session()
    jobs_query = session.query(Jobs, User).join(
        User, Jobs.team_leader == User.id)
    jobs = []
    for job, user in jobs_query:
        jobs.append({
            'title': job.job,
            'leader': f"{user.name} {user.surname}",
            'duration': f"{job.work_size} hours",
            'collaborators': [c.strip() for c in job.collaborators.split(',')],
            'is_finished': job.is_finished
        })

    return render_template('index.html', jobs=jobs)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.register_blueprint(bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(add_job.bp)
    db_session.global_init("db/mars_explorer.db")
    login_manager.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=8080)
