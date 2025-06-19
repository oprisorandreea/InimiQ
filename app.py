from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, re, pandas as pd, pickle
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cheie-secreta'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    chest_pain = db.Column(db.String(10))
    exercise_angina = db.Column(db.String(3))
    fasting_bs = db.Column(db.Integer)
    resting_bp = db.Column(db.Integer)
    max_hr = db.Column(db.Integer)
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Date greșite. Încearcă din nou.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        confirm = request.form['confirm'].strip()

        if '@' not in email or '.' not in email:
            flash('Email invalid.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Email sau username deja folosit.', 'danger')
            return redirect(url_for('register'))

        if password != confirm:
            flash('Parolele nu se potrivesc.', 'danger')
            return redirect(url_for('register'))

        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cont creat cu succes.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            input_data = {
                'Age': int(request.form['age']),
                'Sex': int(request.form['sex']),
                'ChestPainType': request.form['cp'],
                'ExerciseAngina': request.form['exang'],
                'FastingBS': int(request.form['fbs']),
                'RestingBP': int(request.form['restbp']),
                'MaxHR': int(request.form['maxhr'])
            }

            df_input = pd.DataFrame([input_data])

            model_path = os.path.join(basedir, 'model', 'model.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modelul nu a fost găsit la {model_path}. Asigură-te că ai rulat train_model.py")

            with open(model_path, 'rb') as f:
                model = pickle.load(f)

            expected_cols = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else df_input.columns
            for col in expected_cols:
                if col not in df_input.columns:
                    df_input[col] = 0
            df_input = df_input[expected_cols]

            proba = model.predict_proba(df_input)[0][1]
            procent = round(proba * 100, 2)

            pred = Prediction(
                user_id=session['user_id'],
                age=input_data['Age'],
                sex=input_data['Sex'],
                chest_pain=input_data['ChestPainType'],
                exercise_angina=input_data['ExerciseAngina'],
                fasting_bs=input_data['FastingBS'],
                resting_bp=input_data['RestingBP'],
                max_hr=input_data['MaxHR'],
                score=procent
            )
            db.session.add(pred)
            db.session.commit()

            mesaj = f"Pe baza datelor introduse, riscul estimat de predispoziție la o afecțiune cardiovasculară este de aproximativ {procent}%."

            durere = input_data['ChestPainType']
            varsta = input_data['Age']
            glicemie = input_data['FastingBS']

            if procent >= 70:
                if durere == 'ATA':
                    recomandare = "Scor foarte ridicat și durere tipică – se recomandă evaluare urgentă la un cardiolog specializat în ischemie miocardică."
                elif durere == 'ASY':
                    recomandare = "Scor ridicat, simptome silențioase – consultați un cardiolog pentru teste precum EKG sau ecocardiografie."
                else:
                    recomandare = "Scor ridicat – se recomandă investigații cardiologice suplimentare."

            elif procent >= 50:
                if varsta >= 60:
                    recomandare = "Scor moderat și vârstă avansată – se recomandă evaluare preventivă la medicul cardiolog."
                else:
                    recomandare = "Scor moderat – discutați cu medicul de familie pentru o trimitere la specialist."

            else:
                if glicemie == 1:
                    recomandare = "Risc scăzut, dar glicemie crescută – verificați regulat nivelul glicemiei și adoptați o dietă echilibrată."
                elif durere == 'NAP':
                    recomandare = "Risc scăzut, dar durere toracică atipică prezentă – este recomandat un consult preventiv."
                else:
                    recomandare = "Risc scăzut detectat. Continuați un stil de viață sănătos și activ."


            return render_template('result.html', prediction=mesaj, recommendation=recomandare)

        except Exception as e:
            return f"Eroare internă: {e}"

    return render_template('predict.html')

@app.route('/istoric')
def istoric():
    if 'username' not in session:
        return redirect(url_for('login'))
    pred_list = Prediction.query.filter_by(user_id=session['user_id']).order_by(Prediction.created_at.asc()).all()

    labels = [p.created_at.strftime('%Y-%m-%d %H:%M') for p in pred_list]
    scores = [p.score for p in pred_list]

    return render_template('istoric.html', predictions=pred_list, labels=labels, scores=scores)


@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Te-ai delogat cu succes.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #app.run(debug=True)
app.run(host='0.0.0.0', port=5000, debug=True)
