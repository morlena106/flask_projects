from flask import render_template, request, redirect, url_for
from app import app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Проверка, что все поля заполнены
        if not name or not email or not message:
            return render_template("contact.html", error="All fields are required.")

        # Логика обработки данных формы (например, сохранение в базу данных, отправка email)
        # Для примера, просто выводим данные в консоль
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # После успешной отправки данных, перенаправляем или показываем сообщение
        return render_template("contact.html", success="Your message has been sent successfully!")

    # Если GET-запрос, просто отдаем шаблон формы
    return render_template("contact.html")

