# Videoflix Backend

Das Backend für die Videoflix-Plattform, entwickelt mit Django und Django REST Framework. Es bietet APIs für die Benutzerverwaltung, Videoverwaltung und Authentifizierung.

---

## 🚀 Features

- **Benutzerverwaltung**: Registrierung, Login und Token-basierte Authentifizierung.
- **Videoverwaltung**: Hochladen, Abrufen und Kategorisieren von Videos.
- **JWT-Authentifizierung**: Sicherer Zugriff auf geschützte Endpunkte.
- **Kategorisierung**: Videos nach Kategorien gruppieren und durchsuchen.
- **Google Cloud Storage**: Speicherung und Abruf von Videos und Thumbnails.

---

## 🛠️ Technologien

- **Python**: Programmiersprache
- **Django**: Web-Framework
- **Django REST Framework**: API-Entwicklung
- **SQLite**: Datenbank 
- **JWT**: Authentifizierung mit JSON Web Tokens
- **Google Cloud Storage**: Speicherung von Videos und Medien.
- **Google Cloud VM**: Hosting des Backends auf einer virtuellen Maschine.
- **Gunicorn**: WSGI-Server für die Ausführung der Django-Anwendung.
- **Nginx**: Reverse Proxy und statische Dateiverwaltung.

---

## ⚙️ Installation und Setup

### 1. Repository klonen
git clone https://github.com/SunnyDevZH/videoflix-backend
cd videoflix-backend

### 2. Virtuelle Umgebung erstellen und aktivieren
python3 -m venv venv
source venv/bin/activate  # Für macOS/Linux
venv\Scripts\activate     # Für Windows

### 3. Abhängigkeiten installieren
pip install -r requirements.txt

### 4. Datenbankmigrationen ausführen
python3 manage.py makemigrations
python3 manage.py migrate

### 5. Dotenv installieren
pip3 install python-dotenv

### 6. Env-Template erstellen
cp .env.template .env

### 7. Superuser erstellen
python3 manage.py createsuperuser

### 8. Entwicklungsserver starten
python3 manage.py runserver

### 9. Anwendung im Browser öffnen
Öffnen Sie die URL http://127.0.0.1:8000, um die Anwendung zu sehen.


## 🐳 Dockers

### 1. Repository klonen
git clone https://github.com/SunnyDevZH/videoflix-backend
cd videoflix-backend

### 2. .env Datei erstellen
cp .env.template .env


### 3. Docker-Container starten
docker-compose up --build

### 4. Datenbankmigrationen ausführen (im laufenden Container)
docker-compose exec web python manage.py migrate


### 5. Optional: Superuser erstellen
docker-compose exec web python manage.py createsuperuser

### 6. Anwendung im Browser öffnen:
http://localhost:8000


## 📧 Kontakt
Email: yannick.vaterlaus.dev@gmail.com

