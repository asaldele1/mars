from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/index/<title>")
@app.route("/<title>")
def index(title: str):
    return render_template("base.html", title=title)


@app.route("/training/<prof>")
def training(prof: str):
    prof = prof.lower()
    if "инженер" in prof or "строитель" in prof:
        tr = "Инженерные тренажеры"
        image = url_for('static', filename='img/engineer.jpg')
    else:
        tr = "Научные симуляторы"
        image = url_for('static', filename='img/simulators.jpg')
    return render_template("training.html", training=tr, image=image)


@app.route("/list_prof/<list_type>")
def list_prof(list_type: str):
    if list_type in ("ol", "ul"):
        return render_template("list_prof.html", list_type=list_type)
    else:
        return render_template("error.html", error="Неизвестный тип списка")


if __name__ == '__main__':
    app.run(port=8080)
