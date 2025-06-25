# InimiQ – Aplicație de estimare a riscului cardiac

## Descriere generală
InimiQ este o aplicație web realizată cu Flask, care estimează riscul de afecțiuni cardiovasculare pe baza unor factori clinici introduși de utilizator. Modelul de învățare automată utilizat este antrenat pe un set de date real (heart.csv) și generează o probabilitate interpretabilă.

## Repository
Codul sursă complet este disponibil la:  
https://github.com/oprisorandreea/InimiQ

Repository-ul conține doar codul sursă. Fișierele binare compilate (`model.pkl`, `users.db`) sunt generate local automat și NU sunt incluse. 

## Pași de compilare (generare model)

1. Deschide terminalul în folderul proiectului.
2. Rulează comanda:
```bash
python train_model.py
```
3. Va fi creat fișierul `model/model.pkl` folosit pentru predicție.

## Pași de instalare și lansare

1. Clonează sau descarcă repository-ul:
```bash
git clone https://github.com/oprisorandreea/InimiQ.git
```

2. Creează un mediu virtual:
```bash
python -m venv venv
```

3. Activează mediul virtual:
```bash
venv\Scripts\activate       # pe Windows
source venv/bin/activate      # pe Linux/macOS
```

4. Instalează dependențele:
```bash
pip install -r requirements.txt
```

5. (Opțional) Dacă modelul nu a fost generat, rulează:
```bash
python train_model.py
```

6. Rulează aplicația:
```bash
python app.py
```

7. Deschide browserul și accesează:
http://localhost:5000

## Notă
- Fișierul `users.db` (baza de date SQLite) este creat automat la prima rulare.
- Aplicația este complet funcțională local, fără a necesita alte componente externe.
