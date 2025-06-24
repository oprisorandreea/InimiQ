InimiQ – Aplicație de estimare a riscului cardiac
=================================================


Repository oficial: https://github.com/oprisorandreea/InimiQ

---

1. Descriere generală
---------------------
InimiQ este o aplicație web dezvoltată cu Flask, care permite estimarea riscului de afecțiuni cardiovasculare pe baza unor factori medicali introduși de utilizator. Evaluarea este realizată cu ajutorul unui model de învățare automată antrenat pe un set de date real (heart.csv).

---

2. Structura proiectului
------------------------
- app.py – fișierul principal al aplicației (logica Flask)
- train_model.py – script pentru antrenarea modelului de predicție
- heart.csv – setul de date utilizat pentru antrenare
- requirements.txt – lista bibliotecilor necesare
- templates/ – interfața aplicației (fișiere HTML)
- static/ – resurse statice (stiluri CSS, imagini)
- model/ – conține modelul antrenat (model.pkl) [exclus din repository]
- instance/ – conține baza de date locală SQLite (users.db) [exclusă din repository]

---

3. Pași de instalare și lansare
-------------------------------
3.1. Configurare mediu virtual
    python -m venv venv
    venv\Scripts\activate  (pe Windows)

3.2. Instalare dependențe
    pip install -r requirements.txt

3.3. Lansare aplicație
    python app.py

    Aplicația va putea fi accesată la adresa: http://localhost:5000

---

4. Utilizare și funcționalități
-------------------------------
- Creare cont nou și autentificare (pagina /register)
- Introducerea datelor medicale relevante
- Estimarea scorului de risc pe baza modelului ML
- Afișarea unei recomandări medicale personalizate
- Vizualizarea istoricelor anterioare ale predicțiilor

    Notă: Parolele utilizatorilor sunt stocate în clar doar în scop demonstrativ. În medii reale se recomandă hashing (ex: bcrypt).

---

5. Modelul de predicție
-----------------------
- Algoritm: RandomForestClassifier (din scikit-learn)
- Script de antrenare: train_model.py
- Output: model/model.pkl – generat local la rulare

---

6. Note privind livrarea
------------------------
Acest repository Git conține întregul cod sursă al aplicației, cu excepția fișierelor binare generate local (model.pkl, users.db). Pentru evaluare, aplicația se poate rula integral în regim local, urmând pașii descriși în secțiunea 3.

Repository-ul poate fi partajat membrilor comisiei de evaluare și coordonatorului la cerere.

---

7. Autor
--------
Nume: Oprișor Andreea
Facultatea: Automatică și Calculatoare
Universitatea: Universitatea Politehnica Timișoara
Anul: 2025
