💓 InimiQ – Aplicație de estimare a riscului cardiac
Repository oficial:
🔗 https://github.com/oprisorandreea/InimiQ

📁 Structura livrabilului
app.py – aplicația principală (Flask)

train_model.py – script pentru antrenarea modelului ML

heart.csv – setul de date folosit la antrenare

requirements.txt – lista pachetelor necesare

templates/ – interfața aplicației (HTML)

static/ – fișiere statice (CSS, imagini)

model/ – conține model.pkl (❗ nu inclus în repo – se generează local)

instance/ – conține users.db (❗ nu inclus în repo – se generează local)

🛠️ Instalare și rulare locală
Creează un mediu virtual și activează-l

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate     # (Windows)
Instalează pachetele necesare

bash
Copy
Edit
pip install -r requirements.txt
Rulează aplicația

bash
Copy
Edit
python app.py
Accesează aplicația în browser
👉 http://localhost:5000

🧠 Modelul de predicție
Antrenat cu train_model.py pe setul heart.csv

Se salvează local ca model/model.pkl

Utilizează algoritmul RandomForestClassifier (scikit-learn)

🔐 Autentificare demo
Creează un cont nou din aplicație (pagina /register)

Parolele sunt salvate în clar doar în scop demonstrativ

În producție, se recomandă hashing (ex: bcrypt)

⚠️ Note de livrare
Fișierele binare (users.db, model.pkl) sunt excluse din Git prin .gitignore

Acestea se generează local automat la rularea aplicației și a modelului

👤 Autor
Nume: Oprișor Andreea
Facultate: Automatică și Calculatoare, UPT
An: 2025

