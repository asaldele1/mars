from flask import Flask, redirect, render_template, url_for

from forms.login import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


@app.route("/index/<title>")
@app.route("/<title>")
def index(title: str):
    return render_template("base.html", title=title)


@app.route("/training/<prof>")
def training(prof: str):
    prof = prof.lower()
    if "инженер" in prof or "строитель" in prof:
        tr = "Инженерные тренажеры"
        image = url_for("static", filename="img/engineer.jpg")
    else:
        tr = "Научные симуляторы"
        image = url_for("static", filename="img/simulators.jpg")
    return render_template("training.html", training=tr, image=image)


@app.route("/list_prof/<list_type>")
def list_prof(list_type: str):
    if list_type in ("ol", "ul"):
        return render_template("list_prof.html", list_type=list_type)
    else:
        return render_template("error.html", error="Неизвестный тип списка")


@app.route("/answer")
@app.route("/auto_answer")
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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/success")
    return render_template("login.html", title="Авариный доступ", form=form)


@app.route("/success")
def success():
    return render_template("success.html", title="Успех")


@app.route("/distribution")
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


@app.route("/table/<gender>/<int:age>")
def cabin_decor(gender: str, age: int):
    if gender == "female":
        wall_color = "#FFA07A" if age < 21 else "#FF4500"
    else:
        wall_color = "#B0C4DE" if age < 21 else "#007FF0"

    alien_image = "alien_young.png" if age < 21 else "alien_old.png"

    return render_template("table.html",
                           wall_color=wall_color,
                           alien_image=alien_image)


if __name__ == "__main__":
    app.run(port=8080)
