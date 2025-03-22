from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "my_secret_key"  # Для flash-сообщений
db = SQLAlchemy(app)

# Модель агента (таблица)
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    access_level = db.Column(db.String(50), nullable=False)  # Например, "Секретно", "Совершенно секретно"

    def __repr__(self):
        return f"<Agent {self.code_name}>"

# Создаем таблицу, если она не существует
with app.app_context():
    db.create_all()

# Функция генерации случайного кодового имени
def generate_random_code_name():
    adjectives = ['Shadow', 'Black', 'Silent', 'Ghost', 'Red', 'Silver']
    animals = ['Fox', 'Wolf', 'Hawk', 'Tiger', 'Panther', 'Eagle']
    return f"{random.choice(adjectives)} {random.choice(animals)}"

# Главная страница: список агентов с возможностью фильтрации по уровню доступа
@app.route('/')
def index():
    level = request.args.get('access_level')
    if level:
        agents = Agent.query.filter_by(access_level=level).all()
    else:
        agents = Agent.query.all()
    return render_template('index.html', agents=agents)

# Добавление нового агента
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        code_name = request.form.get('code_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        access_level = request.form.get('access_level')
        # Если поле кодового имени пустое, генерируем случайное имя
        if not code_name.strip():
            code_name = generate_random_code_name()
        new_agent = Agent(code_name=code_name, phone=phone, email=email, access_level=access_level)
        db.session.add(new_agent)
        db.session.commit()
        flash("Agent added successfully!")
        return redirect(url_for('index'))
    return render_template('add_agent.html')

# Просмотр досье агента
@app.route('/agent/<int:id>')
def agent_detail(id):
    agent = Agent.query.get_or_404(id)
    return render_template('agent.html', agent=agent)

# Редактирование агента
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)
    if request.method == 'POST':
        agent.code_name = request.form.get('code_name')
        agent.phone = request.form.get('phone')
        agent.email = request.form.get('email')
        agent.access_level = request.form.get('access_level')
        db.session.commit()
        flash("Agent updated successfully!")
        return redirect(url_for('index'))
    return render_template('edit_agent.html', agent=agent)

# Удаление агента
@app.route('/delete/<int:id>')
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    db.session.delete(agent)
    db.session.commit()
    flash("Agent deleted successfully!")
    return redirect(url_for('index'))

# Секретный режим: удаление всех агентов
@app.route('/delete_all')
def delete_all():
    db.session.query(Agent).delete()
    db.session.commit()
    flash("All agents have been deleted! SECRET MODE ACTIVATED.")
    return redirect(url_for('index'))

# Симуляция отправки срочного сообщения агенту
@app.route('/send_message/<int:id>')
def send_message(id):
    agent = Agent.query.get_or_404(id)
    flash(f"Urgent message sent to {agent.code_name} at {agent.email}!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
